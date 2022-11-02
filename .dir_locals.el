((python-mode
  .
  ((pyvenv-activate . "~/Code/mbag/.venv")
   (eglot-workspace-configuration . ((pylsp (plugins
              (flake8 (enabled . t))
              (black (enabled . t) (cache-config . t))
              (pycodestyle (enabled . nil)))))))))
