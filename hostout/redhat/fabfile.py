import os
import os.path
from fabric import api, contrib


def bootstrap():
    hostout = api.env.get('hostout')
    #Install and Update Dependencies
    user = hostout.options['user']

#    contrib.files.append('%%%(user)s  ALL=(ALL) ALL'%locals(),
#                         '/etc/sudoers', use_sudo=True)
    try:
        api.sudo("egrep \"^\%odas\ \ ALL\=\(ALL\)\ ALL\" \"/etc/sudoers\"",pty=True)
    except:
        api.sudo("echo '%odas  ALL=(ALL) ALL' >> /etc/sudoers",pty=True)

#    contrib.files.append('Defaults:%%%(user)s !requiretty'%locals(),
#                         '/etc/sudoers', use_sudo=True)

    try: 
        api.sudo("egrep \"^Defaults\:\%%%(user)s\ \!requiretty\" \"/etc/sudoers\""%locals(),pty=True)
    except:
        api.sudo("echo 'Defaults:%%%(user)s !requiretty' >> /etc/sudoers"%locals(),pty=True)



#    api.sudo('apt-get -y update')
#    api.sudo('apt-get -y upgrade ')
    
    
    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])

    #api.sudo('yum --help')
    api.sudo('yum -y install gcc gcc-c++ '
            'openssl openssl-devel '
            'libjpeg libjpeg-devel '
            'zlib zlib-devel '
            'libpng libpng-devel '
            'libxml2 libxml2-devel '
            'libxslt libxslt-devel ')

    api.sudo('yum -y install '
             'build-essential '
             'python%(major)s python%(major)s-dev '
             'python-setuptools '
             'python-libxml2 '
             'python-elementtree '
#             'python-celementtree '
             'ncurses-dev '
             'lynx '
             'python-imaging '
             'libjpeg-dev '
             'libfreetype6-dev '
             'zlib1g-dev '
             'libreadline5-dev '
             'zlib1g-dev '
             'libbz2-dev '
             'libssl-dev '
             'libjpeg62-dev '
             % locals())
    # python-profiler?

    #to install Python tools 2.4
    api.sudo('wget http://peak.telecommunity.com/dist/ez_setup.py')
    api.sudo('python%(major)s ez_setup.py' % locals())

    #to install PIL
    api.sudo('easy_install-%(major)s --find-links http://download.zope.org/distribution PILwoTK' % locals())
    api.sudo('easy_install-%(major)s --find-links http://dist.repoze.org/PIL-1.1.6.tar.gz PIL' % locals())

    #if its ok you will see something like this:
    #--------------------------------------------------------------------

    #*** TKINTER support not available

    #--- JPEG support ok

    #--- ZLIB (PNG/ZIP) support ok

    #--- FREETYPE2 support ok

    #--------------------------------------------------------------------

    # Add the plone user:

    owner = api.env['buildout-user']
    effective = api.env['effective-user']
    buildoutgroup = api.env['buildout-group']
    
    api.sudo('egrep %(owner)s /etc/passwd || adduser %(owner)s ' % locals())
    api.sudo('egrep %(effective)s /etc/passwd || adduser %(effective)s' % locals())
    api.sudo('gpasswd -a %(owner)s %(buildoutgroup)s' % locals())
    api.sudo('gpasswd -a %(effective)s %(buildoutgroup)s' % locals())


    hostout.setaccess()

    path = api.env.path
    api.sudo('mkdir -p %(path)s' % locals())
    hostout.setowners()
    
    #install buildout
#    api.sudo('easy_install-%(major)s zc.buildout' % locals())
    api.env.cwd = api.env.path
    api.sudo('wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py')
    api.sudo('echo "[buildout]" > buildout.cfg')
    api.sudo('python%(major)s bootstrap.py' % locals())

#    api.sudo('buildout init')
#    api.run('cd /%(path)s && bin/buildout install lxml' % locals())
#    api.run('cd /%(path)s && bin/buildout' % locals())



