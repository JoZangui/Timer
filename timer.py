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
        # Índice do elemento selecionado (hora - 0, minuto - 1, segundo - 2)
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

    # estado do tempo (pausado ou rodando).
    # Se o valor for None o timer está pausado se não o timer está rodando
    _time_is_running = None

    # estado do temporizador (inativo ou ativo), 
    # true para ativo e false para inativo
    """
    Obs: diferente do _time_is_running, o _timer_is_active não verifica se o tempo está pausado
    mas sim se está parado (todos os valores em zero) ou não (esteja esse pausado ou rodando).
    """ 
    _timer_is_active = False

    # funções para habilitar e desabilitar eventos de teclado dependendo de qual tele está ativa (temporizador ou relógio)
    def on_enter(self, *args):
        """
            Função Kivy on_enter:

            É disparado quando a tela é exibida: isto é, quando a animação de entrada está concluída.
            
            Usamos aqui para habilitar todos os eventos de teclado quando entramos na tela do temporizador,
            excepto o evento _go_to_timer

            ver: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
        """
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_down=self._go_to_timer)

    def on_pre_leave(self, *args):
        """
            Função Kivy on_pre_leave:

            É disparado quando a tela está prestes a ser removida: isto é, quando a animação de saída é iniciada.
        
            Usamos aqui para desabilitar todos os eventos de teclado ao sairmos da tela do temporizador para a tela do relógio,
            exceto evento _go_to_timer

            ver: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
        """

        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_down=self._go_to_timer)


    # funções para configurar o temporizador
    def _set_elements_color(self, color):
        """ define a cor de hora, minuto e segundo """
        time_elements = (
            self.label_hour,
            self.label_minute,
            self.label_second
        )

        for element in time_elements:
            element.color = color

    def next_element(self, time_elements):
        """
        vai para o próximo elemento do temporizador

        essa função é usada para navegar entre os elementos do temporizador (hora, minuto, segundo)
        da esquerda para a direita, ele muda a cor do elemento selecionado para vermelho, e os elementos
        não selecionados para cinza

        """
        # configura as cores de todos elementos para cinza
        self._set_elements_color((178, 190, 181))

        # passa para o próximo elemento do timer se o elemento atual não for o último
        if self.index < 2:
            self.index += 1

        # configura a cor do elemento para vermelho
        time_elements[self.index].color = (1, 0, 0)

    def previous_element(self, time_elements):
        """
        vai para o próximo elemento do temporizador

        essa função é usada para navegar entre os elementos do temporizador (hora, minuto, segundo)
        da direita para esquerda, ele muda a cor do elemento selecionado para vermelho, e os elementos
        não selecionados para cinza

        """
        # configura as cores de todos elementos para cinza
        self._set_elements_color((178, 190, 181))

        # passa para o elemento anterior do timer se o elemento atual não for o primeiro
        if self.index > 0:
            self.index -= 1

        # configura a cor do elemento para vermelho
        time_elements[self.index].color = (1, 0, 0)

    def increase_time(self):
        """ Aumenta o tempo """
        hour = int(self.label_hour.text)
        minute = int(self.label_minute.text)
        second = int(self.label_second.text)

        if self.index == 0 and hour < 99:
            self.label_hour.text = str(hour + 1)
        elif self.index == 1 and minute < 59:
            self.label_minute.text = str(minute + 1)
        elif self.index == 2 and second < 59:
            self.label_second.text = str(second + 1)

    def decrease_time(self):
        """ reduz o tempo """
        hour = int(self.label_hour.text)
        minute = int(self.label_minute.text)
        second = int(self.label_second.text)

        if self.index == 0 and hour > 0:
            self.label_hour.text = str(hour - 1)
        elif self.index == 1 and minute > 0:
            self.label_minute.text = str(minute - 1)
        elif self.index == 2 and second > 0:
            self.label_second.text = str(second - 1)

    def _start_timer(self, time_elements):
        # inicia o temporizador
        if (sum(map(lambda element: int(element.text), time_elements)) > 0):
            self._time_is_running = k_prope.Clock.schedule_interval(self.countdown, 1)

            # configura a cor para vermelho
            self._set_elements_color(color=(1,0,0))

            # define o estado do temporizador como activo
            self._timer_is_active = True

            self.label_first_colon.color = (1,0,0)
            self.label_second_colon.color = (1,0,0)

    def _stop_timer(self, time_elements):
        # para o timer

        k_prope.Clock.unschedule(self.countdown)

        for element in time_elements:
            element.text = '0'

        # configura o indice ou ponteiro do temporizador para o primeiro elemento(isto é, para hora)
        self.index = 0

        # define a cor de todos elementos para cinza
        self._set_elements_color((178, 190, 181))
        # define a cor do primeiro elementos para vermelho
        time_elements[0].color = (1, 0, 0)

        if self.sound.state == 'play':
            self.sound.stop()

        self._timer_is_active = False

        self.label_first_colon.color = (178, 190, 181)
        self.label_second_colon.color = (178, 190, 181)

    def _pause_timer(self):
        # pausar ou retornar o temporizador

        if self._time_is_running != None:
            # pausa o timer se estiver rodando
            self._time_is_running = k_prope.Clock.unschedule(self.countdown)
        else:
            # retorna se não estiver rodando
            self._time_is_running = k_prope.Clock.schedule_interval(self.countdown, 1)



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
        if self._timer_is_active == False:
            if keycode[1] == 'right':
                self.next_element(time_elements)

            if keycode[1] == 'left':
                self.previous_element(time_elements)

            if keycode[1] == 'up':
                self.increase_time()

            if keycode[1] == 'down':
                self.decrease_time()

            if keycode[1] == 'enter':
                self._start_timer(time_elements=time_elements)
        else:
            if keycode[1] == 'enter':
                self._stop_timer(time_elements=time_elements)

            if keycode[1] == 'spacebar':
                self._pause_timer()

        if keycode[1] == 'escape':
            message_box = MessageBox()
            message_box.open()
            # keyboard.release()

        if text == 'c':
            # muda para o relógio
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