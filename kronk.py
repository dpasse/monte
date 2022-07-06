import time
import subprocess


if __name__ == '__main__':

    while True:

        print('running...')
        print()

        start_time = time.time()

        response = subprocess.run(
            ['make', 'run_imagineering_jobs'],
            capture_output=True,
            text=True
        )

        print('took:', time.time() - start_time)
        print()

        print("stdout:", response.stdout)
        print("stderr:", response.stderr)
        print()

        print('sleeping...')
        print()

        time.sleep(1 * 60 * 60 * 4) ## 4 hours
