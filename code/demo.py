import subprocess
import time

while True:
    subprocess.call(['./real_time_recv.sh'])
    arr = read_channels('../raw_data/realtime/latest_monitor', plot=False, ylim=[1.0,2.5])
    arr_matrix = stack_channels(arr)
    test_eig = [pca_eigenvalues(arr_matrix)[0]]

    log_result=log_reg.predict(test_eig)
    log_prob=log_reg.predict_proba(test_eig)
    print(log_result, log_prob)
    subprocess.call(['./real_time_send.sh', str(int(log_result)), str(log_prob[0,0]), str(log_prob[0,1])])
    time.sleep(1)