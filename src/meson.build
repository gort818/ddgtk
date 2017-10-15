pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'ddgtk')
gnome = import('gnome')

gnome.compile_resources('ddgtk',
  'ddgtk.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
r= run_command('chmod','755','ddgtk.in')
if r.returncode() != 0
  # it failed
endif
configure_file(
  input: 'ddgtk.in',
  output: 'ddgtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),

)


ddgtk_sources = [
  '__init__.py',
  'gi_composites.py',
  'main.py',
]

install_data(ddgtk_sources, install_dir: moduledir)
