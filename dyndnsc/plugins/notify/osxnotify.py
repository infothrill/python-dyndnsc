# -*- coding: utf-8 -*-

"""
Python integration with OS X's notification center.

Inspired by https://github.com/maranas/pyNotificationCenter
"""

import Foundation  # @UnresolvedImport pylint: disable=import-error
import objc  # @UnresolvedImport pylint: disable=import-error

from ..base import Plugin

NSUSERNOTIFICATION = objc.lookUpClass("NSUserNotification")
NSUSERNOTIFICATIONCENTER = objc.lookUpClass("NSUserNotificationCenter")


def nsnotify(title, subtitle, info_text, delay=0, sound=False, user_info=None):
    """Show a desktop notification on OS X 10.8+.

    :param title: Title of notification
    :param subtitle: Subtitle of notification
    :param info_text: Informative text of notification
    :param delay: Delay (in seconds) before showing the notification
    :param sound: Play the default notification sound
    :param user_info: a dictionary that can be used to handle clicks in your
        app's applicationDidFinishLaunching:aNotification method
    """
    # logging.debug("os x notify called")
    if user_info is None:
        user_info = {}
    notification = NSUSERNOTIFICATION.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(user_info)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUSERNOTIFICATIONCENTER.defaultUserNotificationCenter().scheduleNotification_(notification)


class OSXNotification(object):
    """The OS X notification center notifier."""

    default_title = "Dynamic DNS"
    application_name = "dyndnsc"

    def notify(self, caller, event, message):
        """
        Send a notification.

        :param caller: string caller
        :param event: string event
        :param message: string message
        """
        nsnotify(self.default_title, subtitle=None, info_text=message)


class OSXNotifyPlugin(Plugin):
    """Send desktop notifications with OS X notification center."""

    name = "osxnotify"
    can_configure = True

    def initialize(self):
        """Initialize."""
        self.osxnotification = OSXNotification()

    def after_remote_ip_update(self, ip, status):
        """
        Handle the after_remote_ip_update plugin hook.

        :param ip: ip address
        :param status: string
        """
        if status == 0:
            self.osxnotification.notify(self, None, "Remote IP updated to %s" % ip)
        else:
            self.osxnotification.notify(self, None, "Problem updating remote IP to %s" % ip)
