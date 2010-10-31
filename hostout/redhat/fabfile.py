from fabric import api


def bootstrap():
    hostout = api.env.get('hostout')
    #Install and Update Dependencies
    user = hostout.options['user']

#    contrib.files.append('%%%(user)s  ALL=(ALL) ALL' % dict(user=user),
#                         '/etc/sudoers', use_sudo=True)
    try:
        api.sudo("egrep \"^\%odas\ \ ALL\=\(ALL\)\ ALL\" \"/etc/sudoers\"",pty=True)
    except:
        api.sudo("echo '%odas  ALL=(ALL) ALL' >> /etc/sudoers",pty=True)

#    contrib.files.append('Defaults:%%%(user)s !requiretty' % dict(user=user),
#                         '/etc/sudoers', use_sudo=True)

    try:
        api.sudo("egrep \"^Defaults\:\%%%(user)s\ \!requiretty\" \"/etc/sudoers\"" % dict(user=user), pty=True)
    except:
        api.sudo("echo 'Defaults:%%%(user)s !requiretty' >> /etc/sudoers" % dict(user=user), pty=True)


    # Redhat/centos don't have Python 2.6 or 2.7 in stock yum repos, use EPEL.
    # Could also use RPMforge repo: http://dag.wieers.com/rpm/FAQ.php#B
    api.sudo("rpm -Uvh --force http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-4.noarch.rpm")

#    api.sudo('apt-get -y update')
#    api.sudo('apt-get -y upgrade ')

    version = api.env['python-version']
    python_versioned = 'python' + ''.join(version.split('.')[:2])

    api.sudo('yum -y install gcc gcc-c++ '
            'openssl openssl-devel '
            'libjpeg libjpeg-devel '
            'zlib zlib-devel '
            'libpng libpng-devel '
            'libxml2 libxml2-devel '
            'libxslt libxslt-devel ')

    api.sudo('yum -y install '
             python_versioned + ' '
             python_versioned + '-devel 
             'python-setuptools '
             'libxml2-python '
             'python-elementtree '
             'ncurses-devel '
             'lynx '
             'python-imaging '
             'libjpeg-devel '
             'freetype-devel '
             'zlib-devel '
             'readline-devel '
             'bzip2-devel '
             'openssl-devel '
             'libjpeg-devel '
             )

    #to install Python tools 2.4
    api.sudo('wget http://peak.telecommunity.com/dist/ez_setup.py')
    api.sudo(python_versioned + ' ez_setup.py')

    #to install PIL
    easy_install = "easy_install-" + '.'.join(version.split('.')[:2]) #easy_install-2.6
    api.sudo(easy_install + ' --find-links http://download.zope.org/distribution PILwoTK')
    api.sudo(easy_install + ' --find-links http://dist.repoze.org/PIL-1.1.6.tar.gz PIL')

    #if its ok you will see something like this but you need JPEG, PNG:
    #*** TKINTER support not available

    # Add the plone user:
    owner = api.env['buildout-user']
    effective = api.env['effective-user']
    buildoutgroup = api.env['buildout-group']

    api.sudo('egrep %(owner)s /etc/passwd || adduser %(owner)s ' % dict(owner=owner))
    api.sudo('egrep %(effective)s /etc/passwd || adduser %(effective)s' % dict(effective=effective))
    api.sudo('groupadd -f ' + buildoutgroup)
    api.sudo('gpasswd -a %(owner)s %(buildoutgroup)s' % dict(owner=owner, buildoutgroups=buildoutgroups))
    api.sudo('gpasswd -a %(effective)s %(buildoutgroup)s' % dict(effective=effective, buildoutgroups=buildoutgroups))


    path = api.env.path
    api.sudo('mkdir -p %(path)s' % dict(path=path))
    hostout.setowners()

    #install buildout
    api.env.cwd = api.env.path
    api.sudo('wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py')
    api.sudo('echo "[buildout]" > buildout.cfg')
    api.sudo(python_versioned + ' bootstrap.py')
