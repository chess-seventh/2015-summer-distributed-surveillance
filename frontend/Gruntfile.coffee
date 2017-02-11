#######################################
# Build tasks                         #
#                                     #
# Author: Antony Ducommun dit Boudry  #
#######################################

module.exports = (grunt) ->
  # grunt tasks configuration
  grunt.initConfig(
    pkg: grunt.file.readJSON('package.json')

    # cleanup
    clean:
      assets: ['assets/**/*']

    # assets copy
    copy:
      assets:
        files: [
            expand: true
            cwd: 'bower_components/amcharts/dist'
            src: 'amcharts/**/*.js'
            dest: 'assets/javascripts'
          ,
            expand: true
            cwd: 'bower_components/angular'
            src: 'angular.min.js'
            dest: 'assets/javascripts'
          ,
            expand: true
            cwd: 'bower_components/angular-bootstrap'
            src: 'ui-bootstrap-tpls.min.js'
            dest: 'assets/javascripts'
          ,
            expand: true
            cwd: 'bower_components/bootstrap/dist'
            src: 'fonts/**/*'
            dest: 'assets/'
          ,
            expand: true
            cwd: 'bower_components/bootstrap/dist/css'
            src: 'bootstrap.min.css'
            dest: 'assets/stylesheets'
          ,
            expand: true
            cwd: 'bower_components/fontawesome/css'
            src: 'font-awesome.min.css'
            dest: 'assets/stylesheets'
          ,
            expand: true
            cwd: 'bower_components/fontawesome/'
            src: 'fonts/**/*'
            dest: 'assets/'
          ,
            expand: true
            cwd: 'bower_components/jquery/dist'
            src: 'jquery.min.js'
            dest: 'assets/javascripts'
          ,
            expand: true
            cwd: 'bower_components/moment/min/'
            src: 'moment-with-locales.min.js'
            dest: 'assets/javascripts'
        ]

    # jade templates compilations
    jade:
      app:
        files:
          [
            expand: true
            cwd: 'app/'
            src: ['**/*.jade']
            dest: 'assets/'
            ext: '.html'
          ]
        options:
          pretty: true
          data:
            livereload: false
      app_dev:
        files:
          [
            expand: true
            cwd: 'app/'
            src: ['**/*.jade']
            dest: 'assets/'
            ext: '.html'
          ]
        options:
          pretty: true
          data:
            livereload: true

    # less stylesheets compilation
    less:
      app:
        files:
          [
            expand: true
            cwd: 'app/stylesheets/'
            src: ['**/*.less']
            dest: 'assets/stylesheets/'
            ext: '.css'
          ]
        options:
          sourceMap: true

    # coffee scripts compilation
    coffee:
      app:
        files:
          [
            expand: true
            cwd: 'app/javascripts/'
            src: ['**/*.coffee']
            dest: 'assets/javascripts/'
            ext: '.js'
          ]
        options:
          sourceMap: true

    # file watches
    watch:
      options:
        livereload: true
        spawn: false
      grunt:
        files: 'Gruntfile.coffee'
        options:
          reload: true
      jade:
        files: 'app/**/*.jade'
        tasks: ['jade:app']
      less:
        files: 'app/stylesheets/**/*.less'
        tasks: ['less:app']
      coffee:
        files: 'app/javascripts/**/*.coffee'
        tasks: ['coffee:app']
  )


  # load plugins
  grunt.loadNpmTasks('grunt-contrib-clean')
  grunt.loadNpmTasks('grunt-contrib-copy')

  grunt.loadNpmTasks('grunt-contrib-less')

  grunt.loadNpmTasks('grunt-contrib-coffee')

  grunt.loadNpmTasks('grunt-contrib-jade')

  grunt.loadNpmTasks('grunt-contrib-watch')


  # compile-development task: development processing
  grunt.registerTask(
    'default',
    [
      'clean'
      'copy:assets'
      'jade:app'
      'less:app'
      'coffee:app'
    ]
  )

  grunt.registerTask(
    'dev',
    [
      'clean'
      'copy:assets'
      'jade:app_dev'
      'less:app'
      'coffee:app'
      'watch'
    ]
  )
