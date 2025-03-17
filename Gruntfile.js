module.exports = function(grunt) {
  grunt.initConfig({
    copy: {
      fontawesome: {
        expand: true,
        cwd: 'node_modules/@fortawesome/fontawesome-free/webfonts',
        src: '*',
        dest: 'pytorch_sphinx_theme2/static/webfonts/'
      }
    },
    sass: {
      options: {
        implementation: require('sass'),
        includePaths: ['node_modules']
      },
      dist: {
        options: {
          style: 'expanded'
        },
        files: {
          'pytorch_sphinx_theme2/static/css/theme.css': 'pytorch_sphinx_theme2/static/scss/main.scss'
        }
      }
    },
    concat: {
      options: {
        separator: ';',
      },
      dist: {
        src: ['pytorch_sphinx_theme2/static/js/*.js'],
        dest: 'pytorch_sphinx_theme2/static/js/theme.js',
      },
    },
    watch: {
      css: {
        files: ['pytorch_sphinx_theme2/static/scss/*.scss'],
        tasks: ['sass']
      },
      js: {
        files: ['pytorch_sphinx_theme2/static/js/*.js'],
        tasks: ['concat']
      }
    },
    shell: {
      reinstall: {
        command: 'pip uninstall -y pytorch_sphinx_theme2 && pip install -e .'
      },
      sphinx: {
        command: 'cd docs && rm -rf _build && PYTHONPATH=.. sphinx-build -b html . _build/html'
      }
    },
    connect: {
      server: {
        options: {
          port: 8000,
          base: 'docs/_build/html',
          livereload: true,
          open: true
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-contrib-connect');


  grunt.registerTask('docs', ['copy:fontawesome', 'sass', 'concat', 'shell:reinstall', 'shell:sphinx', 'connect:server', 'watch']);
  grunt.registerTask('default', ['copy:fontawesome', 'sass', 'concat']);
};
