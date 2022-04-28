
with open('/home/ejiang/MuonBDTPid/hash_file_final.txt') as local,open("/home/ejiang/MuonBDTPid/mu_down.txt") as mu_down, open("/home/ejiang/MuonBDTPid/mu_up.txt") as mu_up, open("/home/ejiang/MuonBDTPid/kpi_down.txt") as kpi_down, open("/home/ejiang/MuonBDTPid/kpi_up.txt") as kpi_up, open("/home/ejiang/MuonBDTPid/p_down.txt") as p_down, open("/home/ejiang/MuonBDTPid/p_up.txt") as p_up:
    mu_down_lines = mu_down.read().splitlines()
    mu_up_lines = mu_up.read().splitlines()
    kpi_down_lines = kpi_down.read().splitlines()
    kpi_up_lines = kpi_up.read().splitlines()
    p_down_lines = p_down.read().splitlines()
    p_up_lines = p_up.read().splitlines()
    read_local = local.read()
    for line in mu_down_lines:
        if line in read_local:
            print(1)
        else:
            print(-1)
    for line in mu_up_lines:
        if line in read_local:
            print(1)
        else:
            print(-1)
    for line in kpi_down_lines:
        if line in read_local:
            print(1)
        else:
            print(-1)
    for line in kpi_up_lines:
        if line in read_local:
            print(1)
        else:
            print(-1)
    for line in p_down_lines:
        if line in read_local:
            print(1)
        else:
            print(-1)
    for line in p_up_lines:
        if line in read_local:
            print(1)
        else:
            print(-1)
