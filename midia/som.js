/* SOM-INICIO: copiado de midia/som.js por scripts/sincronizar_som.py (edite lá, não aqui) */
// Sons sintetizados na hora com a Web Audio do navegador: nenhum arquivo, nenhuma rede.
// Começa ligado (quem decide é quem usa). Cada som dura menos de 1 segundo.
var Som = (function () {
  var ctx = null, ligado = false;

  function contexto() {
    if (!ctx) {
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return null;
      ctx = new C();
    }
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  }

  // Uma nota: frequência (Hz), começo e duração (s), tipo de onda, volume e frequência final.
  function nota(c, freq, inicio, dur, tipo, vol, freqFim) {
    var t = c.currentTime + inicio, osc = c.createOscillator(), g = c.createGain();
    osc.type = tipo || "sine";
    osc.frequency.setValueAtTime(freq, t);
    if (freqFim) osc.frequency.exponentialRampToValueAtTime(freqFim, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.2, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g); g.connect(c.destination);
    osc.start(t); osc.stop(t + dur + 0.02);
  }

  // Chiado filtrado (torcida, chute na bola).
  function ruido(c, inicio, dur, vol, freq) {
    var t = c.currentTime + inicio, n = Math.floor(c.sampleRate * dur);
    var buf = c.createBuffer(1, n, c.sampleRate), d = buf.getChannelData(0);
    for (var i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
    var fonte = c.createBufferSource(), filtro = c.createBiquadFilter(), g = c.createGain();
    fonte.buffer = buf;
    filtro.type = "bandpass"; filtro.frequency.value = freq || 1000;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.2, t + dur * 0.4);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    fonte.connect(filtro); filtro.connect(g); g.connect(c.destination);
    fonte.start(t); fonte.stop(t + dur);
  }

  var sons = {
    apito: function (c) { nota(c, 2600, 0, 0.18, "square", 0.05); nota(c, 2600, 0.24, 0.4, "square", 0.05); },
    chute: function (c) { ruido(c, 0, 0.07, 0.4, 700); nota(c, 160, 0, 0.12, "sine", 0.4, 60); },
    gol: function (c) {
      [523, 659, 784, 1047].forEach(function (f, i) { nota(c, f, i * 0.09, 0.22, "triangle", 0.18); });
    },
    torcida: function (c) { ruido(c, 0, 0.9, 0.18, 1200); ruido(c, 0.05, 0.8, 0.1, 600); },
    defesa: function (c) { nota(c, 220, 0, 0.15, "sine", 0.3, 90); },
    erro: function (c) { nota(c, 440, 0, 0.16, "triangle", 0.12); nota(c, 370, 0.16, 0.24, "triangle", 0.12); },
    clique: function (c) { nota(c, 880, 0, 0.05, "sine", 0.08); }
  };

  function tocar(nome) {
    if (!ligado || !sons[nome]) return;
    var c = contexto();
    if (!c) return;
    try { sons[nome](c); } catch (e) {}
  }

  // Liga um botão 🔇/🔊 (ele mesmo mostra o estado).
  function botao(el) {
    function pintar() {
      el.textContent = ligado ? "🔊" : "🔇";
      el.setAttribute("aria-label", ligado ? "Desligar o som" : "Ligar o som");
    }
    el.addEventListener("pointerdown", function (e) {
      e.preventDefault(); e.stopPropagation();
      ligado = !ligado;
      if (ligado) { contexto(); tocar("clique"); }
      pintar();
    });
    pintar();
  }

  return {
    tocar: tocar,
    botao: botao,
    ligar: function (sim) { ligado = !!sim; if (ligado) contexto(); },
    ligado: function () { return ligado; }
  };
})();
/* SOM-FIM */
