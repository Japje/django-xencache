from urlparse import urlparse
import XenAPI
import pprint
from models import *

pp = pprint.PrettyPrinter(depth=6)


def create_session(host, username, password):
    try:
        session = XenAPI.Session('https://' + host)
        session.xenapi.login_with_password(username, password)
    except Exception, e:
        if hasattr(e, 'details') and e.details[0] == 'HOST_IS_SLAVE':
            # Redirect to cluster master
            url = urlparse('https://' + host).scheme + '://' + e.details[1]
            session = XenAPI.Session(url)
            session.login_with_password(username, password)
        else:
            raise Exception(e)
    return session


def get_networks(session):
    data = session.xenapi.network.get_all_records()
    return data


def save_network(session, ref, network):
    if not XenCacheNetwork.objects.filter(opaqueref=ref):
        _create_new_network(ref, network)
    else:
        _update_network(ref, network)


def _create_new_network(ref, data):
    obj = XenCacheNetwork(
        opaqueref=ref,
        uuid=data['uuid'],
        name_label=data['name_label'],
        name_description=data['name_description'],
        other_config=data['other_config'],
        mtu=data['MTU'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheNetwork object" + str(e))


def _update_network(ref, data):
    try:
        obj = XenCacheNetwork.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            name_label=data['name_label'],
            name_description=data['name_description'],
            other_config=data['other_config'],
            mtu=data['MTU'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheNetwork object" + str(e))


def get_srs(session):
    data = session.xenapi.SR.get_all_records()
    return data


def save_sr(session, ref, sr):
    if not XenCacheSR.objects.filter(opaqueref=ref):
        _create_new_sr(ref, sr)
    else:
        _update_sr(ref, sr)


def _create_new_sr(ref, data):
    obj = XenCacheSR(
        opaqueref=ref,
        uuid=data['uuid'],
        name_label=data['name_label'],
        name_description=data['name_description'],
        virtual_allocation=data['virtual_allocation'],
        physical_utilisation=data['physical_utilisation'],
        physical_size=data['physical_size'],
        sr_type=data['type'],
        content_type=data['content_type'],
        shared=data['shared'],
        other_config=data['other_config'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheSR object" + str(e))


def _update_sr(ref, data):
    try:
        obj = XenCacheSR.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            name_label=data['name_label'],
            name_description=data['name_description'],
            virtual_allocation=data['virtual_allocation'],
            physical_utilisation=data['physical_utilisation'],
            physical_size=data['physical_size'],
            sr_type=data['type'],
            content_type=data['content_type'],
            shared=data['shared'],
            other_config=data['other_config'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheSR object" + str(e))


def get_hosts(session):
    data = session.xenapi.host.get_all_records()
    return data


def save_host(session, ref, host):
    if not XenCacheHost.objects.filter(opaqueref=ref):
        _create_new_host(session, ref, host)
    else:
        _update_host(session, ref, host)


def _create_new_host(session, ref, data):
    metric_ref = session.xenapi.host.get_metrics(ref)
    metrics = session.xenapi.host_metrics.get_record(metric_ref)

    obj = XenCacheHost(
        opaqueref=ref,
        uuid=data['uuid'],
        name_label=data['name_label'],
        name_description=data['name_description'],
        memory_overhead=data['memory_overhead'],
        memory_total=metrics['memory_total'],
        memory_free=metrics['memory_free'],
        other_config=data['other_config'],
        cpu_configuration=data['cpu_configuration'],
        cpu_info=data['cpu_info'],
        hostname=data['hostname'],
        address=data['address'],
        edition=data['edition'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheHost object" + str(e))


def _update_host(session, ref, data):
    try:
        metric_ref = session.xenapi.host.get_metrics(ref)
        metrics = session.xenapi.host_metrics.get_record(metric_ref)
        obj = XenCacheHost.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            name_label=data['name_label'],
            name_description=data['name_description'],
            memory_overhead=data['memory_overhead'],
            memory_total=metrics['memory_total'],
            memory_free=metrics['memory_free'],
            other_config=data['other_config'],
            cpu_configuration=data['cpu_configuration'],
            cpu_info=data['cpu_info'],
            hostname=data['hostname'],
            address=data['address'],
            edition=data['edition'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheHost object" + str(e))


def get_vdis(session):
    data = session.xenapi.VDI.get_all_records()
    return data


def save_vdi(session, ref, vdi):
    if not XenCacheVDI.objects.filter(opaqueref=ref):
        _create_new_vdi(ref, vdi)
    else:
        _update_vdi(ref, vdi)


def _create_new_vdi(ref, data):
    sr = XenCacheSR.objects.get(opaqueref=data['SR'],)
    obj = XenCacheVDI(
        opaqueref=ref,
        uuid=data['uuid'],
        name_label=data['name_label'],
        name_description=data['name_description'],
        sr=sr,
        virtual_size=data['virtual_size'],
        physical_utilisation=data['physical_utilisation'],
        vdi_type=data['type'],
        sharable=data['sharable'],
        read_only=data['read_only'],
        other_config=data['other_config'],
        xenstore_data=data['xenstore_data'],
        is_a_snapshot=data['is_a_snapshot'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheVDI object" + str(e))


def _update_vdi(ref, data):
    try:
        sr = XenCacheSR.objects.get(opaqueref=data['SR'],)
        obj = XenCacheVDI.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            name_label=data['name_label'],
            name_description=data['name_description'],
            sr=sr,
            virtual_size=data['virtual_size'],
            physical_utilisation=data['physical_utilisation'],
            vdi_type=data['type'],
            sharable=data['sharable'],
            read_only=data['read_only'],
            other_config=data['other_config'],
            xenstore_data=data['xenstore_data'],
            is_a_snapshot=data['is_a_snapshot'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheVDI object" + str(e))


def get_pifs(session):
    data = session.xenapi.PIF.get_all_records()
    return data


def save_pif(session, ref, pif):
    if not XenCachePIF.objects.filter(opaqueref=ref):
        _create_new_pif(ref, pif)
    else:
        _update_pif(ref, pif)


def _create_new_pif(ref, data):
    network = XenCacheNetwork.objects.get(opaqueref=data['network'],)
    host = XenCacheHost.objects.get(opaqueref=data['host'],)
    obj = XenCachePIF(
        opaqueref=ref,
        uuid=data['uuid'],
        device=data['device'],
        network=network,
        host=host,
        mac=data['MAC'],
        mtu=data['MTU'],
        vlan=data['VLAN'],
        physical=data['physical'],
        currently_attached=data['currently_attached'],
        ip_configuration_mode=data['ip_configuration_mode'],
        netmask=data['netmask'],
        gateway=data['gateway'],
        dns=data['DNS'],
        other_config=data['other_config'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheVDI object" + str(e))


def _update_pif(ref, data):
    try:
        network = XenCacheNetwork.objects.get(opaqueref=data['network'],)
        host = XenCacheHost.objects.get(opaqueref=data['host'],)
        obj = XenCachePIF.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            device=data['device'],
            network=network,
            host=host,
            mac=data['MAC'],
            mtu=data['MTU'],
            vlan=data['VLAN'],
            physical=data['physical'],
            currently_attached=data['currently_attached'],
            ip_configuration_mode=data['ip_configuration_mode'],
            netmask=data['netmask'],
            gateway=data['gateway'],
            dns=data['DNS'],
            other_config=data['other_config'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheVDI object" + str(e))


def get_vms(session):
    data = session.xenapi.VM.get_all_records()
    return data


def save_vm(session, ref, vm):
    if not XenCacheVM.objects.filter(opaqueref=ref):
        _create_new_vm(ref, vm)
    else:
        _update_vm(ref, vm)


def _create_new_vm(ref, data):
    if not data['resident_on'] == 'OpaqueRef:NULL':
        resident_on = XenCacheHost.objects.get(opaqueref=data['resident_on'],)
    else:
        resident_on = None

    obj = XenCacheVM(
        opaqueref=ref,
        uuid=data['uuid'],
        power_state=data['power_state'],
        name_label=data['name_label'],
        name_description=data['name_description'],
        is_a_template=data['is_a_template'],
        resident_on=resident_on,
        memory_overhead=data['memory_overhead'],
        memory_target=data['memory_target'],
        memory_static_max=data['memory_static_max'],
        memory_static_min=data['memory_static_min'],
        memory_dynamic_max=data['memory_dynamic_max'],
        memory_dynamic_min=data['memory_dynamic_min'],
        vcpus_max=data['VCPUs_max'],
        vcpus_at_startup=data['VCPUs_at_startup'],
        other_config=data['other_config'],
        is_control_domain=data['is_control_domain'],
        xenstore_data=data['xenstore_data'],
        is_a_snapshot=data['is_a_snapshot'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheVM object" + str(e))


def _update_vm(ref, data):
    try:
        if not data['resident_on'] == 'OpaqueRef:NULL':
            resident_on = XenCacheHost.objects.get(opaqueref=data['resident_on'],)
        else:
            resident_on = None
        obj = XenCacheVM.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            power_state=data['power_state'],
            name_label=data['name_label'],
            name_description=data['name_description'],
            is_a_template=data['is_a_template'],
            resident_on=resident_on,
            memory_overhead=data['memory_overhead'],
            memory_target=data['memory_target'],
            memory_static_max=data['memory_static_max'],
            memory_static_min=data['memory_static_min'],
            memory_dynamic_max=data['memory_dynamic_max'],
            memory_dynamic_min=data['memory_dynamic_min'],
            vcpus_max=data['VCPUs_max'],
            vcpus_at_startup=data['VCPUs_at_startup'],
            other_config=data['other_config'],
            is_control_domain=data['is_control_domain'],
            xenstore_data=data['xenstore_data'],
            is_a_snapshot=data['is_a_snapshot'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheVM object" + str(e))


def get_vifs(session):
    data = session.xenapi.VIF.get_all_records()
    return data


def save_vif(session, ref, vif):
    if not XenCacheVIF.objects.filter(opaqueref=ref):
        _create_new_vif(ref, vif)
    else:
        _update_vif(ref, vif)


def _create_new_vif(ref, data):
    vm = XenCacheVM.objects.get(opaqueref=data['VM'],)
    network = XenCacheNetwork.objects.get(opaqueref=data['network'],)

    obj = XenCacheVIF(
        opaqueref=ref,
        uuid=data['uuid'],
        device=data['device'],
        network=network,
        vm=vm,
        mac=data['MAC'],
        mtu=data['MTU'],
        other_config=data['other_config'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheVIF object" + str(e))


def _update_vif(ref, data):
    try:
        vm = XenCacheVM.objects.get(opaqueref=data['VM'],)
        network = XenCacheNetwork.objects.get(opaqueref=data['network'],)
        obj = XenCacheVIF.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            device=data['device'],
            network=network,
            vm=vm,
            mac=data['MAC'],
            mtu=data['MTU'],
            other_config=data['other_config'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheVIF object" + str(e))


def get_vbds(session):
    data = session.xenapi.VBD.get_all_records()
    return data


def save_vbd(session, ref, vbd):
    if not XenCacheVBD.objects.filter(opaqueref=ref):
        _create_new_vbd(ref, vbd)
    else:
        _update_vbd(ref, vbd)


def _create_new_vbd(ref, data):
    vm = XenCacheVM.objects.get(opaqueref=data['VM'],)
    if not data['VDI'] == 'OpaqueRef:NULL':
        vdi = XenCacheVDI.objects.get(opaqueref=data['VDI'],)
    else:
        vdi = None
    obj = XenCacheVBD(
        opaqueref=ref,
        uuid=data['uuid'],
        vm=vm,
        vdi=vdi,
        device=data['device'],
        userdevice=data['userdevice'],
        bootable=data['bootable'],
        mode=data['mode'],
        vbd_type=data['type'],
        other_config=data['other_config'],
        currently_attached=data['currently_attached'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCacheVBD object" + str(e))


def _update_vbd(ref, data):
    try:
        vm = XenCacheVM.objects.get(opaqueref=data['VM'],)
        if not data['VDI'] == 'OpaqueRef:NULL':
            vdi = XenCacheVDI.objects.get(opaqueref=data['VDI'],)
        else:
            vdi = None
        obj = XenCacheVBD.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            vm=vm,
            vdi=vdi,
            device=data['device'],
            userdevice=data['userdevice'],
            bootable=data['bootable'],
            mode=data['mode'],
            vbd_type=data['type'],
            other_config=data['other_config'],
            currently_attached=data['currently_attached'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheVBD object" + str(e))


def get_pbds(session):
    data = session.xenapi.PBD.get_all_records()
    return data


def save_pbd(session, ref, pbd):
    if not XenCachePBD.objects.filter(opaqueref=ref):
        _create_new_pbd(ref, pbd)
    else:
        _update_pbd(ref, pbd)


def _create_new_pbd(ref, data):
    host = XenCacheHost.objects.get(opaqueref=data['host'],)
    sr = XenCacheSR.objects.get(opaqueref=data['SR'],)
    obj = XenCachePBD(
        opaqueref=ref,
        uuid=data['uuid'],
        host=host,
        sr=sr,
        currently_attached=data['currently_attached'],
        other_config=data['other_config'],
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCachePBD object" + str(e))


def _update_pbd(ref, data):
    try:
        host = XenCacheHost.objects.get(opaqueref=data['host'],)
        sr = XenCacheSR.objects.get(opaqueref=data['SR'],)
        obj = XenCachePBD.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            host=host,
            sr=sr,
            currently_attached=data['currently_attached'],
            other_config=data['other_config'],
        )
    except Exception, e:
        raise Exception("Could not update XenCacheVBD object" + str(e))


def get_pool(session):
    data = session.xenapi.pool.get_all_records()
    return data


def save_pool(session, ref, pool):
    if not XenCachePool.objects.filter(opaqueref=ref):
        _create_new_pool(ref, pool)
    else:
        _update_pool(ref, pool)


def _create_new_pool(ref, data):
    master = XenCacheHost.objects.get(opaqueref=data['master'],)
    if not data['default_SR'] == 'OpaqueRef:NULL':
        sr = XenCacheSR.objects.get(opaqueref=data['default_SR'],)
    else:
        sr = None

    obj = XenCachePool(
        opaqueref=ref,
        uuid=data['uuid'],
        name_label=data['name_label'],
        name_description=data['name_description'],
        master=master,
        default_sr=sr,
    )
    try:
        obj.clean()
        obj.save()
    except Exception, e:
        raise Exception("Could not create XenCachePool object" + str(e))


def _update_pool(ref, data):
    try:
        master = XenCacheHost.objects.get(opaqueref=data['master'],)
        if not data['default_SR'] == 'OpaqueRef:NULL':
            sr = XenCacheSR.objects.get(opaqueref=data['default_SR'],)
        else:
            sr = None

        obj = XenCachePool.objects.filter(opaqueref=ref).update(
            uuid=data['uuid'],
            name_label=data['name_label'],
            name_description=data['name_description'],
            master=master,
            default_sr=sr,
        )
    except Exception, e:
        raise Exception("Could not update XenCachePool object" + str(e))


def fetch_data():
    for pool in Pool.objects.all():
        master = pool.members.first()
        session = create_session(master.fqdn, pool.username, pool.password)

        # save/update Networks
        networks = get_networks(session)
        for network in networks:
            save_network(session, network, networks[network])

        # save/update Storage Repositories
        srs = get_srs(session)
        for sr in srs:
            save_sr(session, sr, srs[sr])

        # save/update Hosts
        hosts = get_hosts(session)
        for host in hosts:
            save_host(session, host, hosts[host])

        # save/update Virtual Disk Images
        vdis = get_vdis(session)
        for vdi in vdis:
            save_vdi(session, vdi, vdis[vdi])

        # save/update Physical InterFaces
        pifs = get_pifs(session)
        for pif in pifs:
            save_pif(session, pif, pifs[pif])

        # save/update Virtual Machines
        vms = get_vms(session)
        for vm in vms:
            save_vm(session, vm, vms[vm])

        # save/update Virtual InterFaces
        vifs = get_vifs(session)
        for vif in vifs:
            save_vif(session, vif, vifs[vif])

        # save/update Virtual Block Devices
        vbds = get_vbds(session)
        for vbd in vbds:
            save_vbd(session, vbd, vbds[vbd])

        # save/update Virtual Block Devices
        pbds = get_pbds(session)
        for pbd in pbds:
            save_pbd(session, pbd, pbds[pbd])

        # save/update Pool information
        pools = get_pool(session)
        for pool in pools:
            save_pool(session, pool, pools[pool])
