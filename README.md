# qe_GaN
Datasets and input files for calculating GaN properties by quantum-espresso

Set up ubuntu

After you install ubuntu OS in your PC, first thing to do is update and upgrade pre-installed programs.

sudo apt update
sudo apt upgrade -y

And then, install quantum-espresso

sudo apt install -y quantum-espresso

Checking the installation of quantum-espresso, do pw.x

pw.x

If you have message like this, stop the application by Ctrl + C

Next, install emacs, which is editor software.

sudo apt install -y emacs

And, install python and python3-pip

sudo apt install -y python
sudo apt install -y python3-pip

Next, install gnuplot for drawing graphs

sudo apt install -y gnuplot-x11

Next, install git

sudo apt install -y git

If your laguage is Japanese, recommend to following setting.
日本語を使っている場合、ドキュメントやピクチャなどのフォルダパスを英語名に変更することを勧める。

LANG=C xdg-user-dirs-gtk-update

立ち上がるウィンドウの指示に従って、変更すればよい。

Finally, make directry for calculation

mkdir work

directory name can be canged as you like.
git clone this project in your work directry.


