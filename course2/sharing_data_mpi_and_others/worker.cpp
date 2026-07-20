#include <iostream>
#include <random>
#include <dragon/dictionary.hpp>
#include <dragon/serializable.hpp>

int main(int argc, char* argv[]) {
    try {
        const char* ser_ddict = argv[1];
        std::string iterations_str = argv[2];
        std::string samples_per_iteration_str = argv[3];
        int iterations = std::stoi(iterations_str);
        int samples_per_iteration = std::stoi(samples_per_iteration_str);
        DDict<Serializable, Serializable> ddict(ser_ddict, nullptr);
        int proc_id = ddict.fetch_add("worker_id");

        std::cout <<"Worker " << proc_id << " says: Hello!" << std::endl;

        for (int i=0; i<iterations; i++) {
            // The following waits until this value is available for this checkpoint
            // because of wait_for_keys on the ddict.
            std::cout << "Worker " << proc_id << " waiting for pi from orchestrator." << std::endl;
            double pi = ddict["pi"];

            // modern C++ random number generation
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_real_distribution<double> distrib(0.0, 1.0);

            int inside_circle = 0;
            for (int j=0; j<samples_per_iteration; j++) {
                double x_coord = distrib(gen);
                double y_coord = distrib(gen);
                if (x_coord * x_coord + y_coord * y_coord <= 1.0)
                    inside_circle += 1;
            }

            pi = (pi + (4.0 * inside_circle / samples_per_iteration))/2;

            std::cout << "Proc " << proc_id << " providing its update for pi=" << pi << std::endl;
            std::string key_str = "worker" + std::to_string(proc_id);
            SerializableString key = key_str;
            ddict[key] = pi;
            ddict.checkpoint();
        }

    } catch (DragonError ex) {
        std::cout << "Got error " << ex << std::endl;
    }

    return 0;
}