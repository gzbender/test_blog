test-blog:
  django_addr: http://127.0.0.1:8000
  port: 8000
  server_name: test-blog.loc
  venv_dir: /home/vagrant/env/test-blog-env
  work_dir: /test_blog
  settings: test_blog_project
  log_file: /test_blog/log/log.txt
  error_log_file: /test_blog/log/error_log.txt
  workers_count: 3
  run_user: vagrant
  run_group: vagrant


python2:
  lookup:
    pkg: python2.7

mysql:
  charset: utf8
  server:
    root_password: 'somepass'
    bind-address: 127.0.0.1
    port: 3306
    user: mysql

  # Manage databases
  database:
    - name: blog_service
      charset: utf8
  schema:
    blog:
      load: False

  # Manage users
  user:
    - name: blog_service
      password: 'somepass'
      host: localhost
      databases:
        - database: blog_service
          grants: ['all privileges']