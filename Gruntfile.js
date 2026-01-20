module.exports = function(grunt) {
  grunt.initConfig({
    copy: {
      fontawesome: {
        files: [
          {
            expand: true,
            cwd: 'node_modules/@fortawesome/fontawesome-free/webfonts',
            src: '*',
            dest: 'pytorch_sphinx_theme2/static/webfonts/'
          },
          {
            expand: true,
            cwd: 'node_modules/@fortawesome/fontawesome-free/css',
            src: 'all.min.css',
            dest: 'pytorch_sphinx_theme2/static/webfonts/'
          }
        ]
      }
    },
    clean: {
      css: ['pytorch_sphinx_theme2/static/css/theme.css'],
      js: ['pytorch_sphinx_theme2/static/js/theme.js']
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
        command: 'uv pip uninstall pytorch_sphinx_theme2 && uv pip install -e .'
      },
      sphinx: {
        command: 'cd docs && rm -rf _build && PYTHONPATH=.. sphinx-build -b html . _build/html'
      }
    },
    connect: {
      server: {
        options: {
          port: 3000,
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
  grunt.loadNpmTasks('grunt-contrib-clean');



  grunt.registerTask('docs', ['clean', 'copy:fontawesome', 'sass', 'concat', 'shell:reinstall', 'shell:sphinx', 'connect:server', 'watch']);
  grunt.registerTask('default', ['clean', 'copy:fontawesome', 'sass', 'concat']);
};
