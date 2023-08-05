# -*- coding: utf-8 -*-
"""Módulo principal del programa StwEx."""

__author__ = "Germán Sánchez Gutiérrez"
__contact__ = "gsgsoftgroup@gmail.com"
__version__ = "0.1.1"

import logging
# import time
import os, sys
import wx
import wx.adv
import argparse
import time, signal
import xml.etree.ElementTree as ET

import shlex, subprocess
import threading
import re

TOOLTIP = "StwEx " + __version__
variables = {}  # Diccionario de variables globales definidas a partir del fichero XML de configuración.
default_mainIcon = "images/logoStwex.png"
global tsk


class Action():
    '''Clase Action.
    Acciones definidas en el fichero XML de configuración.'''

    def __init__(self, id, cmd, terminal=False, killonexit=True, relaunch=False, filecomm=None):
        """
        Método init de la clase Action.1
        :param id: Identificador de la acción. Si es -1 se ejecuta al inicializar la aplicación.
        :param cmd: Comando que se ejecuta en la acción.
        :param terminal: Se ejecuta el comando en una terminal
        :param killonexit: Se mata el proceso cuando se cierra la aplicación. Tiene que estar la variable killallonexit a True.
        :param relaunch:
        :param filecomm: Fichero temporal de comunicación.
        """
        self.id = id
        self.cmd = cmd
        self.terminal = terminal
        self.killonexit = killonexit
        # TODO: No se ha implementado un sistema para relanzar la acción si termina antes de cerrar la aplicación.
        # La variable relaunch todavía no tiene utilidad.
        self.relaunch = relaunch
        self.filecomm = filecomm
        self.filecomm_opened = False
        self.commThread = None  # Objeto de comunicación
        self.exitcomm = False
        self.PID = None
        self.stdout = None

        logging.debug("Nueva Action definida:")
        logging.debug("-- id: " + self.id)
        logging.debug("-- cmd: " + self.cmd)
        logging.debug("-- killonexit: " + str(self.killonexit))
        logging.debug("-- terminal: " + str(self.terminal))
        logging.debug("-- relaunch: " + str(self.relaunch))
        logging.debug("-- filecomm: " + str(self.filecomm))
        logging.debug("-----------------------------")

    def exec_cmd(self):
        """
        Ejecuta el comando asociado a la acción.
        :return:
        """
        if self.filecomm:
            if self.cmd == "@default":
                # @default se encarga de crear un proceso por defecto sólo para tener el fichero de comunicación.
                self.cmd = "echo"

        args = shlex.split(self.cmd)
        try:
            if self.terminal:
                # TODO: Más opciones xterm para definir tamaño de la ventana
                commando = "xterm -hold -e " + self.cmd
                args = shlex.split(commando)

            p = subprocess.Popen(args, stderr=self.stdout)

            if self.filecomm is not None:
                # Si hay fichero de comunicación se ejecuta el hilo de comunicación.
                self.commThread = threading.Thread(target=self.comm, name='Thread-ID' + self.id)
                self.commThread.start()
            self.PID = p.pid
        except:
            logging.info("Error al ejecutar: " + self.cmd)

    def kill(self):
        """
        Mata al proceso asociado a la acción.
        :return:
        """
        if self.PID != None:
            if self.killonexit == True:  # Sólo se mata si la variable killonexit es True
                logging.debug("Matando al proceso " + str(self.PID) + " - killonexit: " + str(self.killonexit))
                self.exitcomm = True  # Matando el hilo de comunicación
                try:
                    os.kill(self.PID, 9)
                except:
                    logging.info("No existe el proceso " + str(self.PID))

    def order_comm(self, order):
        """
        Ejecuta la orden pasada por el fichero de comunicación.
        :param order: Comando de comunicación. No confundir con el comando asociado a la acción.
        :return:
        """
        delimiter = "##"
        patron = re.compile("(?P<order>\[STWEX:.*\])(?P<argumento>.*)", re.IGNORECASE)
        m = patron.search(order)
        if m:
            # Orden: [stwex:icon] - Cambia el taskbark icon
            if m.group('order').lower() == "[stwex:icon]":
                if os.path.isfile(m.group('argumento')):
                    global tsk
                    wx.CallAfter(tsk.OnSetIcon, m.group('argumento'))

            # Orden: [stwex:show_message] - Muestra un mensaje de notificación en pantalla
            if m.group('order').lower() == "[stwex:show_message]":
                campos = m.group('argumento').split(delimiter)
                if len(campos) == 3:  # Title, Message and Flags
                    nmsg = wx.adv.NotificationMessage(title=campos[0], message=campos[1])
                    if campos[2].lower() == "error":
                        nmsg.SetFlags(wx.ICON_ERROR)
                    elif campos[2].lower() == "warning":
                        nmsg.SetFlags(wx.ICON_WARNING)
                    else:
                        # nmsg.SetFlags(wx.ICON_INFORMATION)
                        if os.path.isfile(campos[2]):
                            nmsg.SetIcon(wx.Icon(campos[2]))
                elif len(campos) == 2:  # Title and message
                    nmsg = wx.adv.NotificationMessage(title=campos[0], message=campos[1])
                    nmsg.SetFlags(wx.ICON_INFORMATION)
                else:  # Only message
                    nmsg = wx.adv.NotificationMessage(title=TOOLTIP, message=m.group('argumento'))
                    nmsg.SetFlags(wx.ICON_INFORMATION)
                # nmsg.SetFlags(wx.ICON_INFORMATION)
                nmsg.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)

            # Orden: [stwex:var] - Se define una variable global o se cambia su valor.
            if m.group('order').lower() == "[stwex:var]":
                campos = m.group('argumento').split(delimiter)
                if len(campos) == 2:  # Key and value
                    key = campos[0]
                    key = "@" + str(key)
                    value = campos[1]
                    variables[key] = value

    def comm(self):
        """
        Método de comunicación con el fichero de comunicación (filecomm).
        Este método se ejecuta en un hilo aparte.
        :return:
        """
        if self.filecomm:
            # En el siguiente bucle while se intenta abrir el fichero de comunicación cada segundo
            file_communication = None
            while ((not self.filecomm_opened) & (not self.exitcomm)):
                if not self.filecomm_opened:
                    try:
                        file_communication = open(self.filecomm)
                        self.filecomm_opened = True
                    except:
                        logging.info("No hay fichero de comunicación " + self.filecomm)
                    time.sleep(5)

            position = 0
            sinlectura = 0
            while (not self.exitcomm):
                line = file_communication.readline()
                # print("Bucle while lectura de :" + str(position) + ":" + line )
                if not line:
                    # print(file_communication.closed)
                    if sinlectura > 10:  # El valor de las veces que no se debe leer nada para reabrir el fichero puede ser ajustada.
                        sinlectura = 0
                        # Después de muchas pruebas, se comprobó que para asegurar la lectura correcta del
                        # fichero se debería de cerrar y abrir de nuevo si no se leía nada durante X veces.
                        logging.debug("Cerrando y abriendo de nuevo el fichero de comunicación " + self.filecomm)
                        file_communication.close()
                        try:
                            file_communication = open(self.filecomm)
                        except:
                            logging.info("No hay fichero de comunicación " + self.filecomm)
                            break
                    sinlectura += 1
                    file_communication.seek(position)
                    time.sleep(1)
                    continue

                sinlectura = 0
                position = file_communication.tell()
                # Se ejecuta el comando de comunicación
                self.order_comm(line)

                time.sleep(1)
                # yield line

            if file_communication:
                file_communication.close()
            self.filecomm_opened = False
        logging.debug("Exiting " + threading.currentThread().getName())


class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Clase que crea el TaskBarIcon principal de la aplicación.
    """

    def __init__(self, frame, file_config):
        """Inicializa un objeto TaskBarIcon

        :parameter file_config: Fichero de configuración de la aplicación
        """

        self.dir_path = os.path.dirname(os.path.realpath(file_config))

        if not os.path.isfile(file_config):
            logging.info("No existe el fichero XML: " + str(file_config))
            help()
            sys.exit(-1)

        self.file_xml = file_config
        self.list_actions = {}
        self.listactions = {}
        # self.listPID_actions = {}

        self.main_cmd = None
        self.main_cmd_pid = None

        # Obteniendo la configuración inicial del documento XML
        with open(self.file_xml, 'rt') as f:
            try:
                tree = ET.parse(f)
            except:
                logging.info("Error al leer el fichero XML.")
                print("El fichero XML es incorrecto.")
                help()
                sys.exit(-1)

        for node in tree.iter('stwex'):
            mainIcon = node.attrib.get('icon')
            if mainIcon:
                mainIcon = os.path.join(self.dir_path, mainIcon)  # Icono que se mostrará en la barra de tareas
            mainTitle = node.attrib.get('title')  # Mensaje que aparecerá cuando se ponga el cursor encima.
            mainKillAll = node.attrib.get(
                'killallonexit')  # Matar los programas ejecutados desde esta aplicación si la variable killonexit de la acción es True.

            logging.debug("NODO:")
            logging.debug("->mainIcon: " + str(mainIcon))
            logging.debug("->mainTitle: " + str(mainTitle))
            logging.debug("->mainKillAll: " + str(mainKillAll))
            logging.debug("----------------")

            break  # Por si hay más de un objeto 'stwex' en el fichero XML sólo lee el primero. NO HE VISTO UN SISTEMA MEJOR

        # Se leen las variables
        for node in tree.iter('variable'):
            # TODO: Se debería comprobar que key no tenga carácteres raros.
            variable_key = node.attrib.get('key')
            variable_key = "@" + str(variable_key)  # Le añadimos una @ al principio
            # TODO: Se debería comprobar que value no tenga carácteres raros.
            variable_value = node.attrib.get('value')
            if variable_key and variable_value:
                variables[variable_key] = variable_value  # Se añade al diccionario global variables

        # Se leen las acciones
        for node in tree.iter('action'):
            action_id = node.attrib.get('id')
            action_cmd = node.attrib.get('cmd')
            action_terminal = node.attrib.get('terminal')

            # action_terminal
            # Por defecto, action_terminal es False
            if action_terminal != None:
                if (action_terminal.lower() in ['true', '1', 't', 'y', 'yes']):
                    action_terminal = True
                else:
                    action_terminal = False
            else:
                action_terminal = False

            # action_killonexit
            # Por defecto, action_killonexit es True
            action_killonexit = node.attrib.get('killonexit')
            if action_killonexit != None:
                if (action_killonexit.lower() in ['false', '0', 'f', 'n', 'no']):
                    action_killonexit = False
                else:
                    action_killonexit = True
            else:
                action_killonexit = True

            # action_relaunch
            # Por defecto, action_relaunch es False
            action_relaunch = node.attrib.get('relaunch')
            if action_relaunch is not None:
                if (action_relaunch.lower() in ['true', '1', 't', 'y', 'yes']):
                    action_relaunch = True
            else:
                action_relaunch = False

            # action_filecomm
            action_filecomm = node.attrib.get('filecomm')

            # action_cmd
            if action_cmd is not None:  # Si no existe el atributo cmd no se añade el 'action'
                action = Action(id=action_id, cmd=action_cmd, killonexit=action_killonexit, terminal=action_terminal,
                                relaunch=action_relaunch, filecomm=action_filecomm)
                self.listactions[action_id] = action

        if mainIcon is not None and os.path.isfile(mainIcon):
            self.icon = mainIcon
        else:
            if hasattr(sys,
                       '_MEIPASS'):  # Si existe, se está ejecutando el ejecutable creado por PYInstaller y las rutas cambian
                self.icon = os.path.join(sys._MEIPASS, default_mainIcon)
            else:
                self.icon = self.dir_path + '/' + default_mainIcon

        self.frame = frame
        self.toggle = 0
        wx.adv.TaskBarIcon.__init__(self)

        if mainTitle == None:
            self.mensaje = TOOLTIP
        else:
            self.mensaje = mainTitle

        if (mainKillAll != None):
            if (mainKillAll.lower() in ['true', '1', 't', 'y', 'yes']):
                self.killAllOnExit = True
        else:
            self.killAllOnExit = False

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OpenMenu)
        self.OnSetIcon(self.icon)

        # Se ejecuta el comando con id -1
        if ("-1" in self.listactions.keys()):
            self.listactions["-1"].exec_cmd()

    def substitution_variable(self, line):
        """
        Sustituye en la linea pasada por parámetros las variables que aparezcan (@variable) por sus valores.

        :param line: Línea a la que se va sustituir las referencias a variables por sus valores.
        :return: Línea modificada
        """
        if line:
            patron = re.compile("(?P<key>@.*)", re.IGNORECASE)  # Los nombres de las variables son case unsensitive
            match = patron.search(line)
            if match:
                key = match.group('key')
                if key in variables.keys():
                    return variables[key]
                else:
                    return line
        return line  # Si no se le pasa nada (None) se devuelve de la misma manera.

    def CreatePopupMenuXML(self, tree):
        """
        Crea el menú Popup a partir de la información XML. Se puede ejecutar de manera recursiva para generar submenús.

        :param tree: Árbol de información XML
        :return:
        """

        # Se lee los distintos elementos del menú (node)
        for node in tree.iter('menu'):
            menu = wx.Menu()
            # for myItem in node.iter("item"):
            for myItem in node:
                if myItem.tag == 'item':
                    title = myItem.attrib.get('title')
                    title = self.substitution_variable(title)

                    action = myItem.attrib.get('action')
                    action = self.substitution_variable(action)

                    icono = myItem.attrib.get('icon')
                    shortcut = myItem.attrib.get('shortcut')
                    enable_option = myItem.attrib.get('enable')
                    hidden_option = myItem.attrib.get('hidden')

                    if title:
                        logging.debug("title: " + title)
                    if action:
                        logging.debug("action: " + action)
                    if icono:
                        icono = os.path.join(self.dir_path, icono)
                        logging.debug("icono: " + icono)

                    if title == None:
                        title = "Default"

                    itemMenu = wx.MenuItem(menu, wx.NewId(), title)
                    if (icono != None):
                        if (os.path.isfile(icono)):
                            # TODO: Comprobar que no falla al cargar el bitmap
                            img = wx.Bitmap(icono, wx.BITMAP_TYPE_ANY)
                            itemMenu.SetBitmap(wx.Bitmap(img))

                    if shortcut != None:
                        # entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord(shortcut), itemMenu.GetId())
                        entry = wx.AcceleratorEntry()
                        entry.FromString(shortcut)
                        itemMenu.SetAccel(entry)

                    appendElement = True
                    for itemsubmenu in myItem:
                        if itemsubmenu.tag == 'submenu':
                            submenu = self.CreatePopupMenuXML(itemsubmenu)
                            submenu.Bind(wx.EVT_MENU, self.myAction, id=itemMenu.GetId())
                            itemMenu.SetSubMenu(submenu)
                        if itemsubmenu.tag == 'separator':
                            appendElement = False
                            menu.AppendSeparator()

                    # hidden option. Por defecto es False
                    if hidden_option != None:
                        hidden_option = self.substitution_variable(hidden_option)
                        if hidden_option.lower() in ['true', '1', 't', 'y', 'yes']:
                            # Si hidden_option es True entonces no se añade el elemento
                            appendElement = False
                        else:
                            appendElement = True

                    if appendElement:  # No se tiene que añadir si se ha añadido un separador
                        menu.Append(itemMenu)

                        # Enable se tiene que hacer después de hacer Append al elemento del menú.
                        # Sólo se puede ejecutar esta orden si se ha añadido el elemento del menú.
                        if enable_option != None:
                            enable_option = self.substitution_variable(enable_option)
                            if enable_option.lower() in ['true', '1', 't', 'y', 'yes']:
                                itemMenu.Enable(enable=True)
                            else:
                                itemMenu.Enable(enable=False)

                    if (action == "@exit"):
                        menu.Bind(wx.EVT_MENU, self.OnQuit, id=itemMenu.GetId())
                    else:
                        if action != None:
                            # menu.Bind(wx.EVT_MENU, self.myAction, id=itemMenu.GetId())
                            self.list_actions[itemMenu.GetId()] = action
                            menu.Bind(wx.EVT_MENU, self.myAction, id=itemMenu.GetId())
            break
        return menu

    def CreatePopupMenu(self):
        """
        Crea el menú del TaskBarIcon. Se lee el fichero XML y se genera el árbol inicial.
        :return:
        """
        with open(self.file_xml, 'rt') as f:
            tree = ET.parse(f)

        return self.CreatePopupMenuXML(tree)

    # def exec_cmd(self, cmd):
    #     args = shlex.split(cmd)
    #     p = subprocess.Popen(args)
    #     return p.pid

    def myAction(self, event):
        """
        Método que ejecuta una acción cuando se lanza el evento al pulsar sobre una opción del menú.

        :param event:
        :return:
        """
        id = event.GetId()
        myaction = self.list_actions[id]  # Obtengo el id del 'action'
        logging.debug("myaction: " + myaction)
        if (myaction in self.listactions.keys()):
            self.listactions[myaction].exec_cmd()

    def OpenMenu(self, event):
        """
        Open the menu of the TaskBarIcon.

        :param event:
        :return:
        """
        # self.PopupMenu(self.CreatePopupMenu())
        self.PopupMenu(self.CreatePopupMenu())

    # def set_server(self, event):
    #     """Set the default server"""
    #     self.config.set_server(event.GetId())
    #     logging.debug(self.config.get_server())

    def OnSetIcon(self, path):
        """
        Cambia el icono del TaskBarIcon.

        :param path: Ruta del icono.
        :return:
        """
        icon = wx.Icon(path)
        self.SetIcon(icon, self.mensaje)

    def OnQuit(self, event):
        """
        Finaliza la aplicación de manera ordenada matando todas las acciones ejecutadas.

        :param event:
        :return:
        """
        # Se mata todas las acciones que se han ejecutado.
        if self.killAllOnExit:
            for action in self.listactions.values():
                action.kill()
        self.RemoveIcon()
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def UpdateIcons(self):
        """
        Actualiza el TaskBarIcon
        :return:
        """
        # TODO: Este es un método obtenido de otro programa y no sé si realiza alguna acción aquí.
        self.itimer = signal.ITIMER_REAL
        time = int(signal.getitimer(self.itimer)[0])
        if time == 0:
            self.mensaje = TOOLTIP
        else:
            self.mensaje = TOOLTIP + " - " + str(time) + " s"


def help():
    print("StwEx " + __version__)
    print("Usage: stwex [-f file_XML]")


def do_nothing(*evt):
    """
    Función que no hace nada o pequeñas tareas repetitivas.
    Esta función es necesaria para que la aplicación WX reaccione cada X milisegundos y no sólo se dispare por eventos.
    Sin esta función no funcionaría el timeout de la conexión ya que sólo 'reaccionaría' cuando se hiciera clic sobre
    el icono de la aplicación (evento).

    Actualmente esta función actualiza el icono de la barra de tareas.

    :param evt:
    :return:
    """
    global tsk
    tsk.UpdateIcons()


def main():
    """ Programa principal. """
    parser = argparse.ArgumentParser(description='Se conecta con un servidor remoto para gestión remota')
    parser.add_argument('-f', '--file', type=str, nargs='?', default="stwex.xml",
                        help='Fichero de configuración')
    parser.add_argument('-v', '--verbosity', action="count",
                        help='Incrementa los mensajes de salida')
    args = parser.parse_args()

    if args.verbosity:
        if args.verbosity == 1 or args.verbosity == 2:
            logging.basicConfig(
                level=logging.INFO,
                format='(%(threadName)-10s) %(message)s',
            )

        if args.verbosity > 2:
            logging.basicConfig(
                level=logging.DEBUG,
                format='(%(threadName)-10s) %(message)s',
            )

    app = wx.App()
    frame = wx.Frame(None)

    global tsk
    tsk = TaskBarIcon(frame, args.file)

    # El timer es necesario para que la aplicación REACCIONE cada X milisegundos y pueda funcionar signal.
    timer = wx.Timer()
    app.Bind(wx.EVT_TIMER, do_nothing, timer)  # Llamamos a la función do_nothing
    timer.Start(1000)

    app.MainLoop()


if __name__ == '__main__':
    main()
