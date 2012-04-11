import gtk
import pygtk

from model_simple import MyModel
from view import MyView
from controller import MyController

def main():
    m = MyModel()
    v = MyView()
    c = MyController(m, v)
    gtk.main()

if __name__=='__main__':
    main()

