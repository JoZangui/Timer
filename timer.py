from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import kivy.properties as k_prope
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup


class MessageBox(Popup):
    pass

class ClockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        k_prope.Clock.schedule_interval(self.update, 1)

    hour = k_prope.ObjectProperty('0')
    minute = k_prope.ObjectProperty('0')
    second = k_prope.ObjectProperty('0')

    def update(self, *args):
        self.hour = str(datetime.now().hour)
        self.minute = str(datetime.now().minute)
        self.second = str(datetime.now().second)


class TimerScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = SoundLoader.load('audio/mixkit-vintage-warning-alarm-990.ogg')
        self.sound.loop = True
        self.sound.volume = .07
        self.index = 0

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'Text'
        )

        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    label_hour = k_prope.ObjectProperty(None)
    label_minute = k_prope.ObjectProperty(None)
    label_second = k_prope.ObjectProperty(None)

    label_first_colon = k_prope.ObjectProperty(None)
    label_second_colon = k_prope.ObjectProperty(None)

    # stores the state of the Clock object, so we know if the time is running or not
    _time_is_running = None

    # stores the state of the timer, true for active and false for inactive
    # obs: The timer is active when it is not stopped, i.e. time is running or paused but not stopped (not restarted)
    _timer_is_active = False

    # disable and enable keyboard events depending on which screen is displayed
    def on_enter(self, *args):
        """
            enable all keyboard events on enter to timer screen except _go_to_timer
        """
        if self._timer_is_active:
            self._keyboard.bind(on_key_down=self._stop_pause_and_go_to_clock)
        else:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_pre_leave(self, *args):
        """
            disable all keyboard events except events for _go_to_timer between screens
        """
        if self._timer_is_active:
            self._keyboard.unbind(on_key_down=self._stop_pause_and_go_to_clock)
        else:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_down=self._go_to_timer)


    # functions to set the time
    def _set_elements_color(self, color):
        """ set the color of hour, minute and second """
        time_elements = (
            self.label_hour,
            self.label_minute,
            self.label_second
        )

        for element in time_elements:
            element.color = color
        self.label_first_colon.color = color
        self.label_second_colon.color = color

    def next_element(self, time_elements):
        """ go to next element """
        for element in time_elements:
            element.color = (178, 190, 181)

        if self.index < 2:
            self.index += 1
        time_elements[self.index].color = (1, 0, 0)

    def previous_element(self, time_elements):
        """ go to previous element """
        for element in time_elements:
            element.color = (178, 190, 181)

        if self.index > 0:
            self.index -= 1
        time_elements[self.index].color = (1, 0, 0)

    def increase_time(self):
        """ increase the time """
        hour = int(self.label_hour.text)
        minute = int(self.label_minute.text)
        second = int(self.label_second.text)

        if self.index == 0 and hour < 24:
            self.label_hour.text = str(hour + 1)
        elif self.index == 1 and minute < 59:
            self.label_minute.text = str(minute + 1)
        elif self.index == 2 and second < 59:
            self.label_second.text = str(second + 1)

    def decrease_time(self):
        """ decrease de time """
        hour = int(self.label_hour.text)
        minute = int(self.label_minute.text)
        second = int(self.label_second.text)

        if self.index == 0 and hour > 0:
            self.label_hour.text = str(hour - 1)
        elif self.index == 1 and minute > 0:
            self.label_minute.text = str(minute - 1)
        elif self.index == 2 and second > 0:
            self.label_second.text = str(second - 1)


    # keyboard events
    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        time_elements = (
            self.label_hour,
            self.label_minute,
            self.label_second
        )

        if keycode[1] == 'right':
            self.next_element(time_elements)

        if keycode[1] == 'left':
            self.previous_element(time_elements)

        if keycode[1] == 'up':
            self.increase_time()

        if keycode[1] == 'down':
            self.decrease_time()

        if text == 'c':
            # go to clock screen
            self.manager.current = 'Clock'
            self.manager.transition.direction = 'left'

        if keycode[1] == 'enter':
            # start the timer
            if (sum(int(item.text) for item in time_elements) > 0):
                self._time_is_running = k_prope.Clock.schedule_interval(self.countdown, 1)

                # disable all keys
                self._keyboard.unbind(on_key_down=self._on_keyboard_down)

                # enable only enter, spacebar and c text to go to clock screen
                self._keyboard.bind(on_key_down=self._stop_pause_and_go_to_clock)
                
                # set the color to red
                self._set_elements_color(color=(1,0,0))

                # set the timer state to active
                self._timer_is_active = True

        if keycode[1] == 'escape':
            message_box = MessageBox()
            message_box.open()
            # keyboard.release()

        return True

    def _stop_pause_and_go_to_clock(self, keyboard, keycode, text, modifiers):
        """
            Enable only 'enter': to stop the timer,
            'spacebar': to pause the timer,
            and '_stop_pause_and_go_to_clock method': to navigate to clock screen
        """
        time_elements = (
            self.label_hour,
            self.label_minute,
            self.label_second
        )

        if keycode[1] == 'enter':
            # stop the timer
            
            k_prope.Clock.unschedule(self.countdown)

            for element in time_elements:
                element.text = '0'

            # set the index back to 0
            self.index = 0

            # set the color to gray
            self._set_elements_color((178, 190, 181))
            time_elements[0].color = (1, 0, 0)
            
            
            # enable all keys
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

            # disable only _stop_pause_and_go_to_clock method
            self._keyboard.unbind(on_key_down=self._stop_pause_and_go_to_clock)

            if self.sound.state == 'play':
                self.sound.stop()

            self._timer_is_active = False

        if keycode[1] == 'spacebar':
            # pause or start the time

            if self._time_is_running != None:
                # if the time is running, stop
                self._time_is_running = k_prope.Clock.unschedule(self.countdown)
            else:
                # if not, start
                self._time_is_running = k_prope.Clock.schedule_interval(self.countdown, 1)

        if text == 'c':
            # go to clock screen
            self.manager.current = 'Clock'
            self.manager.transition.direction = 'left'

        return True

    def _go_to_timer(self, keyboard, keycode, text, modifiers):
        if text == 't':
            # go to timer screen
            self.manager.current = 'Timer'
            self.manager.transition.direction = 'right'

        if keycode[1] == 'escape':
            message_box = MessageBox()
            message_box.open()
        
        return True


    # counter
    def countdown(self, dt):
        """ count the time """
        hour = int(self.label_hour.text)
        minute = int(self.label_minute.text)
        second = int(self.label_second.text)

        if second > 0:
            self.label_second.text = str(second - 1)
        elif minute > 0:
            self.label_minute.text = str(minute - 1)
            self.label_second.text = '59'
        elif hour > 0:
            self.label_hour.text = str(hour - 1)
            self.label_minute.text = '59'
            self.label_second.text = '59'

        if sum((hour, minute, second)) == 0:
            k_prope.Clock.unschedule(self.countdown)

            if self.sound:
                self.sound.play()


class Main(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (300, 100)
        self.title = "Clock and Timer"

        
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(TimerScreen(name='Timer'))
        screen_manager.add_widget(ClockScreen(name='Clock'))

        return screen_manager


if __name__ == "__main__":
    Main().run()