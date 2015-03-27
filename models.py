from django.db import models
# your models here


class Server(models.Model):
    fqdn = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255, default="")

    def __unicode__(self):
        return self.fqdn

    class Meta:
        ordering = ['fqdn']


class Pool(models.Model):
    name = models.CharField(max_length=64, unique=True)
    members = models.ManyToManyField(Server, related_name='pools')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']


class XenCacheNetwork(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    name_label = models.CharField(max_length=128)
    name_description = models.TextField()
    other_config = models.TextField()
    mtu = models.BigIntegerField()

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCacheSR(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    name_label = models.CharField(max_length=128)
    name_description = models.TextField()
    virtual_allocation = models.BigIntegerField()
    physical_utilisation = models.BigIntegerField()
    physical_size = models.BigIntegerField()
    sr_type = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    shared = models.BooleanField(default=False)
    other_config = models.TextField()

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCacheHost(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    name_label = models.CharField(max_length=128)
    name_description = models.TextField()
    memory_overhead = models.BigIntegerField()
    memory_total = models.BigIntegerField()
    memory_free = models.BigIntegerField()
    other_config = models.TextField()
    cpu_configuration = models.TextField()
    cpu_info = models.TextField()
    hostname = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    edition = models.CharField(max_length=128)

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCacheVDI(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    name_label = models.CharField(max_length=128)
    name_description = models.TextField()
    sr = models.ForeignKey(XenCacheSR, related_name='vdis')
    virtual_size = models.BigIntegerField()
    physical_utilisation = models.BigIntegerField()
    vdi_type = models.CharField(max_length=255)
    sharable = models.BooleanField(default=False)
    read_only = models.BooleanField(default=False)
    other_config = models.TextField()
    xenstore_data = models.TextField()
    is_a_snapshot = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCachePIF(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    device = models.CharField(max_length=128)
    network = models.ForeignKey(XenCacheNetwork, related_name='pifs')
    host = models.ForeignKey(XenCacheHost, related_name='pifs')
    mac = models.CharField(max_length=128)
    mtu = models.BigIntegerField()
    vlan = models.BigIntegerField()
    physical = models.BooleanField(default=False)
    currently_attached = models.BooleanField(default=False)
    ip_configuration_mode = models.CharField(max_length=128)
    netmask = models.CharField(max_length=128)
    gateway = models.CharField(max_length=128)
    dns = models.CharField(max_length=128)
    other_config = models.TextField()

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCacheVM(models.Model):
    POWER_STATES = (
        ('Halted', 'Halted'),
        ('Paused', 'Paused'),
        ('Running', 'Running'),
        ('Suspended', 'Suspended'),
    )
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    power_state = models.CharField(choices=POWER_STATES, max_length=12)
    name_label = models.CharField(max_length=128)
    name_description = models.TextField()
    is_a_template = models.BooleanField(default=False)
    resident_on = models.ForeignKey(XenCacheHost, related_name='vms', null=True)
    memory_overhead = models.BigIntegerField()
    memory_target = models.BigIntegerField()
    memory_static_max = models.BigIntegerField()
    memory_static_min = models.BigIntegerField()
    memory_dynamic_max = models.BigIntegerField()
    memory_dynamic_min = models.BigIntegerField()
    vcpus_max = models.BigIntegerField()
    vcpus_at_startup = models.BigIntegerField()
    other_config = models.TextField()
    is_control_domain = models.BooleanField(default=False)
    xenstore_data = models.TextField()
    is_a_snapshot = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCacheVIF(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    device = models.CharField(max_length=128)
    network = models.ForeignKey(XenCacheNetwork, related_name='vifs')
    vm = models.ForeignKey(XenCacheVM, related_name='vifs')
    mac = models.CharField(max_length=128)
    mtu = models.BigIntegerField()
    other_config = models.TextField()

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCacheVBD(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    vm = models.ForeignKey(XenCacheVM, related_name='vbds')
    vdi = models.ForeignKey(XenCacheVDI, related_name='vbds', null=True)
    device = models.CharField(max_length=128)
    userdevice = models.CharField(max_length=128)
    bootable = models.BooleanField(default=False)
    mode = models.CharField(max_length=128)
    vbd_type = models.CharField(max_length=128)
    other_config = models.TextField()
    currently_attached = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCachePBD(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    host = models.ForeignKey(XenCacheHost, related_name='pbds')
    sr = models.ForeignKey(XenCacheSR, related_name='pbds')
    currently_attached = models.BooleanField(default=False)
    other_config = models.TextField()

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']


class XenCachePool(models.Model):
    opaqueref = models.CharField(max_length=128, unique=True, blank=False)
    uuid = models.CharField(max_length=128)
    name_label = models.CharField(max_length=128)
    name_description = models.TextField()
    master = models.ForeignKey(XenCacheHost, related_name='pools')
    default_sr = models.ForeignKey(XenCacheSR, related_name='pools', null=True)

    def __unicode__(self):
        return unicode(str(self.uuid))

    class Meta:
        ordering = ['uuid']
