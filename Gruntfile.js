module.exports = function(grunt) {

  // load all grunt tasks
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  grunt.initConfig({
    // Read package.json
    pkg: grunt.file.readJSON("package.json"),

    open : {
      dev: {
        path: 'http://localhost:1919'
      }
    },

    connect: {
      server: {
        options: {
          port: 1919,
          base: 'docs/build',
          livereload: true
        }
      }
    },
    copy: {
      fonts: {
        files: [
          {
              expand: true,
              flatten: true,
              src: ['fonts/Lato/*'],
              dest: 'pytorch_sphinx_theme/static/fonts/Lato',
              filter: 'isFile'
          }
        ]
      },

      images: {
        files: [
          {
              expand: true,
              flatten: true,
              src: ['images/*'],
              dest: 'pytorch_sphinx_theme/static/images',
              filter: 'isFile'
          }
        ]
      }
    },

    sass: {
      dev: {
        options: {
          style: 'expanded'
        },
        files: [{
          expand: true,
          cwd: 'scss',
          src: ['*.scss'],
          dest: 'pytorch_sphinx_theme/static/css',
          ext: '.css'
        }]
      },
      build: {
        options: {
          style: 'compressed',
          sourcemap: 'none'
        },
        files: [{
          expand: true,
          cwd: 'scss',
          src: ['*.scss'],
          dest: 'pytorch_sphinx_theme/static/css',
          ext: '.css'
        }]
      }
    },

    browserify: {
      dev: {
        options: {
          external: ['jquery'],
          alias: {
            'pytorch-sphinx-theme': './js/theme.js'
          }
        },
        src: ['js/*.js'],
        dest: 'pytorch_sphinx_theme/static/js/theme.js'
      },
      build: {
        options: {
          external: ['jquery'],
          alias: {
            'pytorch-sphinx-theme': './js/theme.js'
          }
        },
        src: ['js/*.js'],
        dest: 'pytorch_sphinx_theme/static/js/theme.js'
      }
    },
    uglify: {
      dist: {
        options: {
          sourceMap: false,
          mangle: {
            reserved: ['jQuery'] // Leave 'jQuery' identifier unchanged
          },
          ie8: true // compliance with IE 6-8 quirks
        },
        files: [{
          expand: true,
          src: ['pytorch_sphinx_theme/static/js/*.js', '!pytorch_sphinx_theme/static/js/*.min.js'],
          dest: 'pytorch_sphinx_theme/static/js/',
          rename: function (dst, src) {
            // Use unminified file name for minified file
            return src;
          }
        }]
      }
    },
    usebanner: {
      dist: {
        options: {
          position: 'top',
          banner: '/* <%= pkg.name %> version <%= pkg.version %> | MIT license */\n' +
                  '/* Built <%= grunt.template.today("yyyymmdd HH:mm") %> */',
          linebreak: true
        },
        files: {
          src: [ 'pytorch_sphinx_theme/static/js/theme.js', 'pytorch_sphinx_theme/static/css/theme.css' ]
        }
      }
    },
    exec: {
      build_sphinx: {
        cmd: 'sphinx-build ../tutorials/ docs/build'
      }
    },
    clean: {
      build: ["docs/build"],
      fonts: ["pytorch_sphinx_theme/static/fonts"],
      images: ["pytorch_sphinx_theme/static/images"],
      css: ["pytorch_sphinx_theme/static/css"],
      js: ["pytorch_sphinx_theme/static/js/*", "!pytorch_sphinx_theme/static/js/modernizr.min.js"]
    },

    watch: {
      /* Compile scss changes into theme directory */
      sass: {
        files: ['scss/*.scss'],
        tasks: ['sass:dev']
      },
      /* Changes in theme dir rebuild sphinx */
      sphinx: {
        files: ['pytorch_sphinx_theme/**/*', 'README.rst', 'docs/**/*.rst', 'docs/**/*.py'],
        tasks: ['clean:build','exec:build_sphinx']
      },
      /* JavaScript */
      browserify: {
        files: ['js/*.js'],
        tasks: ['browserify:dev']
      },
      /* live-reload the docs if sphinx re-builds */
      livereload: {
        files: ['docs/build/**/*'],
        options: { livereload: true }
      }
    }

  });

  grunt.loadNpmTasks('grunt-exec');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-open');
  grunt.loadNpmTasks('grunt-browserify');

  grunt.registerTask('default', ['clean','copy:fonts', 'copy:images', 'sass:dev','browserify:dev','usebanner','exec:build_sphinx','connect','open','watch']);
  grunt.registerTask('build', ['clean','copy:fonts', 'copy:images', 'sass:build','browserify:build','uglify','usebanner','exec:build_sphinx']);
}
