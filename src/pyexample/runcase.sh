#!/bin/bash
commande=$*
/home/I35256/salome/base/appli_DEV/salome -t
/home/I35256/salome/base/appli_DEV/salome shell $commande
/home/I35256/salome/base/appli_DEV/salome killall
