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
## Código fonte (python)
---
### ClockScreen(Screen)

`ClockScreen` é uma instância da classe Screen, ela nos permite criar uma janela na aplicação. Usamos ela para criar uma janela tanto para o relógio como para o temporizador. Você pode ler mais sobre [Screen](https://kivy.org/doc/stable/api-kivy.modules.screen.html#module-kivy.modules.screen) na documentação do Kivy.

Usamos a função Kivy: `schedule_interval()` para actualizar as informações na nossa aplicação, no caso o tempo, isto dentro de um respectivo intervalo, ela recebe como argumento a função `self.update` (que é responsável por actualizar as informações de hora, minuto e segundo), e o intervalo da actualização, neste caso 1 segundo.

A nossa class tem como atributos: `hour`, `minute` e `second` cada uma delas faz referência a uma label presente em `main.kv`, essa referência é feita através de `ObjectProperty`. Essas labels são responsáveis por apresentar as informações na tela. você pode ver mais sobre isso na sessão [Código fonte (kivy)](#código-fonte-kivy).

```python
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
```
---
### TimerScreen(Screen)

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