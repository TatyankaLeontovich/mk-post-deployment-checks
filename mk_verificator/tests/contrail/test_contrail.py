def test_contrail_status(local_salt_client):
    cs = local_salt_client.cmd(
        'cpu*', 'cmd.run', ['contrail-status | grep -Pv \'(==|^$)\'']
    )
    broken_services = []

    for node in cs:
        for line in cs[node].split('\n'):
            line = line.strip()
            name, status = line.split(None, 1)
            if status not in {'active'}:
                err_msg = "{node}:{service} - {status}".format(
                    node=node, service=name, status=status)
                broken_services.append(err_msg)

    assert not broken_services, 'Broken services: {}'.format(broken_services)
