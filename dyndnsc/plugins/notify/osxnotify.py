# -*- coding: utf-8 -*-
"""
Python integration with OS X's notification center
Inspired by https://github.com/maranas/pyNotificationCenter
"""

import Foundation
import objc

from ..base import Plugin

_NSUserNotification = objc.lookUpClass('NSUserNotification')
_NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')


def nsnotify(title, subtitle, info_text, delay=0, sound=False, user_info=None):
    """ Python method to show a desktop notification on Mountain Lion. Where:
    title: Title of notification
    subtitle: Subtitle of notification
    info_text: Informative text of notification
    delay: Delay (in seconds) before showing the notification
    sound: Play the default notification sound
    user_info: a dictionary that can be used to handle clicks in your
    app's applicationDidFinishLaunching:aNotification method
    """
    #logging.debug("os x notify called")
    if user_info is None:
        user_info = {}
    notification = _NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(user_info)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    _NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)


class OSXNotification(object):
    default_title = "Dynamic DNS"
    application_name = "dyndnsc"

    def notify(self, caller, event, message):
        nsnotify(self.default_title, subtitle=None, info_text=message)


class OSXNotifyPlugin(Plugin):
    '''
    Send desktop notifications with OS X notification center
    '''
    name = 'osxnotify'
    can_configure = True

    def initialize(self):
        self.osxnotification = OSXNotification()

    def after_remote_ip_update(self, ip, status):
        if status == 0:
            self.osxnotification.notify(self, None, "Remote IP updated to %s" % ip)
        else:
            self.osxnotification.notify(self, None, "Problem updating remote IP to %s" % ip)
