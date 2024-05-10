# kivy Timer and Clock

### Índice

* [Descrição do projecto](#descrição-do-projecto)
* [Funcionalidades](#funcionalidades)
* [Aplicação](#aplicação)
* [Ferramentas usadas](#ferramentas-usadas)
* [Código fonte (python)](#código-fonte-python)
* [Código fonte kivy](#código-fonte-kivy)
* [Acesso ao projecto](#acesso-ao-projecto)
* [Abrir e rodar o projecto](#abrir-e-rodar-o-projecto)
* [Desenvolvedor](#desenvolvedor)


## Descrição do projecto

Temporizador e relógio digital para ajudar na produtividade e na qualidade de vida do desenvolvedor.
Tendo em mente aprender Kivy, decidi criar um Temporizador. Essa ideia surgiu na necessidade de um temporizador para controlar o tempo em que fico codando, visto que o Ubuntu não tem um temporizador, eu decidi criar este enquanto aprendia kivy, sim, quando comecei eu estava usando ubuntu, agora estou usando Windows outra vez, por favor fiquem avontade para explorar este simples projecto.

---
## Funcionalidades

`Funcionalidade 1:` Podemos mudar entre o relógio e o temporizador através das teclas: **T** para o temporizador e **C** para o relógio.

`Funcionalidade 2:`
### Temporizador
O tempo no temporizador é ajustado usando o teclado, seta _**esquerda**_ e _**direita**_ para navegar entre hora, minuto e segundo, as setas _**para cima**_ e _**para baixo**_ são usadas para aumentar ou diminuir o tempo, _**Enter**_ é usado para iniciar e para parar o tempo, _**Espaço**_ é usado para pausar e continuar, _**Esc**_ para fechar a aplicação.

Quando o tempo terminar o temporizador irá emitir um som, para parar basta precionar _**Enter**_.

---
## Aplicação

<img src="video/ReadMe-video.gif"/>

---
## Ferramentas usadas

<div style="display: flex">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png" width="35" title="Python">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/58/Kivy_logo.png" width="35" title="Kivy">
</div>

### Python / Kivy

---
# Código fonte (python)
### ClockScreen(Screen)

`ClockScreen` é uma instância da classe Screen. Screen nos permite criar uma janela na aplicação, usamos ela para criar uma janela tanto para o relógio como para o temporizador.

Você pode ler mais sobre [Screen](https://kivy.org/doc/stable/api-kivy.modules.screen.html#module-kivy.modules.screen) na documentação do Kivy.

Usamos a função Kivy: `schedule_interval()` para actualizar as informações na nossa aplicação, no caso o tempo, isto dentro de um respectivo intervalo, ela recebe como argumento a função `self.update` (que é responsável por actualizar as informações de hora, minuto e segundo), e o intervalo da actualização, neste caso 1 segundo.

A nossa class tem como atributos: `hour`, `minute` e `second` cada uma delas faz referência a uma label presente em `main.kv`, essa referência é feita através de `ObjectProperty`. Essas labels são responsáveis por apresentar as informações na tela. você pode ver mais sobre isso na sessão [Código fonte (kivy)](#código-fonte-kivy).

---
### TimerScreen(Screen)

`TimerScreen` é uma instância da classe Screen. Screen nos permite criar uma janela na aplicação, usamos ela para criar uma janela tanto para o relógio como para o temporizador.

Você pode ler mais sobre [Screen](https://kivy.org/doc/stable/api-kivy.modules.screen.html#module-kivy.modules.screen) na documentação do Kivy.

`TimerScreen` possui os seguintes métodos:

**Eventos disparados em transição de tela**
* [on_enter()](#on_enter)
* [on_pre_leave()](#on_pre_leave)

**Métodos de definição de tempo e estado de temporizador**
* [_set_elements_color()](#_set_elements_color)
* [next_element()](#next_element)
* [previous_element()](#previous_element)
* [increase_time()](#increase_time)
* [decrease_time()](#decrease_time)
* [start_timer()](#start_timer)
* [stop_timer()](#stop_timer)
* [pause_timer()](#pause_timer)

**Eventos de teclado**
* [_on_keyboard_down()](#_on_keyboard_down)
* [go_to_timer()](#go_to_timer)

**Contador**
* [countdown()](#countdown)

# Eventos disparados em transição de tela
## on_enter()
Este método é na verdade um evento Kivy para transição entre telas. Este evento é disparado quando a animação de entrada está concluída, isto é, quando a transição de uma tela para outra está concluída.

Usamos aqui para habilitar todos os eventos de teclado quando entramos na tela do temporizador,
excepto o evento `go_to_timer()`, que é desabilitado.

Você pode ver mais sobre `on_enter()` [na documentação do Kivy](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html)

## on_pre_leave()
`on_pre_leave()` também é uma evento Kivy, este evento é disparado quando a tela está prestes a ser removida, ou seja, quando a animação de saída de uma tela pra outra é iniciada.

Usamos aqui para desabilitar todos os eventos de teclado ao sairmos da tela do temporizador para a tela do relógio,
exceto evento `go_to_timer()` que é habilitado aqui.

Você pode ver mais sobre `go_to_timer()` [na documentação do Kivy](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html)

# Métodos de definição de tempo e estado de temporizador
Esses métodos são usados para controlar o temporizador, como por exemplo: aumentar e reduzir o tempo, selecionar entre hora, minuto e segundo, e por consequência mudar o estado do temporizador para rodando, parado ou pausado. Eles são na maioria usados em [eventos de teclados](#_keyboard_closed).

## _set_elements_color()
`_set_elements_color()` é usado para definir a cor dos elementos do temporizador, ele recebe como argumento a cor a ser definida

## next_element()
`next_element()` é Usado para navegar entre hora, minuto e segundo no temporizador. Ele recebe como argumento os elementos do temporizador no caso hora, minuto e segundo.

## previous_element()
`previous_element()` é usado para navegar entre segundo, minuto e hora no temporizador. Ele recebe como argumento os elementos do temporizador no caso hora, minuto e segundo.

## increase_time()
`increase_time()` é usado para aumentar o tempo.

## decrease_time()
`decrease_time()` é usado para reduzir o tempo.

## start_timer()
`start_timer()` é usado para iniciar o tempo, ele recebe como argumento os elementos do temporizador, hora, minuto e segundo.

## stop_timer()
`stop_timer()` é usado para parar o tempo, ele recebe como argumento os elementos do temporizador, hora, minuto e segundo.

## pause_timer()
`pause_timer()` é usado para pausar ou retomar o tempo.

# Eventos de teclado
Os eventos de teclados são usado para navegar e manipular o temporizador através do teclado. O Timer possui eventos para: navegar entre hora, minuto e segundo, definir o tempo para o temporizador, transitar entre o temporizador e o relógio e muito mais. Muitas dessas opções já abordamos em [Métodos de definição de tempo e estado de temporizador](#_set_elements_color).

## _on_keyboard_down()
`_on_keyboard_down`, é aqui onde usamos boa parte dos eventos de teclado excepto o evento para transitar do relógio para o temporizador.

Ele recebe como argumento `keyboard`, `keycode`, `text`, e `modifiers` que são na maioria usados para ler o estado do teclado, ou seja ela executa uma acção dependendo de qual tecla foi pressionada, e isso é verificado por exemplo através de `keycode` e do `text`.

Para saber mais sobre eventos de teclado, [consulte a documentação do Kivy](https://kivy.org/doc/stable/api-kivy.core.window.html).

## go_to_timer()
`go_to_timer()` é usado para transitar do relógio para o temporizador, ele recebe como argumento `keyboard`, `keycode`, `text`, e `modifiers`. Ele é acionado quando pressionado a tecla `T` no teclado.


# Contador
## countdown()
`countdown()` é usado para contar o tempo, ele trabalha reduzindo o tempo periodicamente, isso é feito através de `k_prope.Clock.schedule_interval(self.countdown, 1)` que chama a função a cada 1(um) segundo, e `k_prope.Clock.unschedule(self.countdown)` que é responsável por para-lo. exemplo:

**Usado para iniciar o temporizador**
```python
def start_timer(self, time_elements:tuple):
    """ inicia o temporizador """
    if (sum(map(lambda element: int(element.text), time_elements)) > 0):
        self._time_is_running = k_prope.Clock.schedule_interval(self.countdown, 1)
```

**Usado para parar o temporizador**
```python
def stop_timer(self, time_elements:tuple):
    """ para o timer """
    k_prope.Clock.unschedule(self.countdown)
```

# Código fonte kivy
## ClockScreen

`<ClockScreen>` é aqui onde trabalhamos todos os elementos visuais da tela do relógio. Ela possui uma `BoxLayout` que é responsável por organizar os elementos visuais em um estilo **boxlayout** semelhante ao **gridlayout** do **CSS (Cascading Style Sheets)**.

Dentro deste `BoxLayout` nós temos: `orientation`, que define a posição dos elementos na tela para **vertical** ou **horizontal**, neste caso ele está definido para **horizontal**, e também temos as diferentes `label` que são usadas para apresentar as informações necessárias na tela.

## TimerScreen
Semelhante ao `<ClockScreen>` nós usamos o `<TimerScreen>` para trabalhar a aparência do temporizador. Ela possui as variáveis (`label_hour`, `label_minute`, `label_second`, `label_first_colon`, `label_second_colon`) que permite a relação entre `TimerScreen()` que está em **Timer.py** e as label de `<TimerScreen>` que está em **main.kv**.

Ela também possui uma `BoxLayout` e dentro dela, uma `orientation` e várias `label` para apresentar as informações na tela.

## MessageBox
Temos também `<MessageBox>` que possui as mesmas caracteristicas que `<ClockScreen>` e `<TimerScreen>`, ela é responsável por apresentar uma mensagem na tela quando pressionamos a tecla **Esc** para fechar o Timer.

---
## Acesso ao projecto
Você pode [acessar o código fonte do projecto](https://github.com/JoZangui/Timer/tree/main)

---
## Abrir e rodar o projecto
Abra o seu terminal no directorio do projecto e digite `python timer.py`.

---
## Desenvolvedor
<div style="width: 100px; overflow: hidden; border-radius: 100%">
    <img src="https://avatars.githubusercontent.com/u/82146261?v=4" width="100">
</div>

[Joaquim Zangui](https://github.com/JoZangui)