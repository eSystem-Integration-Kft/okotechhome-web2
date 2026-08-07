/* Témaváltó — világos / sötét.
 *
 * MIÉRT A `<head>`-BEN, HALASZTÁS NÉLKÜL FUT. A témát a `<html>` `data-theme`
 * attribútuma hordozza. Ha ez a szkript a törzs végén futna, a látogató előbb
 * látná a világos oldalt, és csak utána váltana sötétre — egy villanás minden
 * oldalbetöltéskor. Ezért ez az EGYETLEN szkript, amelyik nem `defer`-rel
 * töltődik: néhány sor, a stíluslap után, még a törzs feldolgozása előtt.
 *
 * MIÉRT NEM A CSS DÖNTI EL. A `prefers-color-scheme` médialekérdezés egyedül
 * nem lenne elég: a látogató választása felülírja a rendszerbeállítást, azt
 * pedig CSS nem tudja. Ha viszont a szkript MINDIG kiírja a feloldott témát,
 * a CSS-nek nem is kell médialekérdezés — egyetlen helyen, a
 * `[data-theme="dark"]` blokkban élnek a sötét tokenek, duplikálás nélkül.
 *
 * JS NÉLKÜL: a `data-theme` sosem kerül ki, az oldal világos marad — ez a
 * teljes értékű alapállapot. A váltógomb ilyenkor NEM jelenik meg (app.css
 * 5.12c), mert egy nem működő kapcsoló rosszabb, mint a hiánya.
 */
(() => {
  'use strict';

  const KULCS = 'oth-tema';
  const gyoker = document.documentElement;
  const rendszerSotet = window.matchMedia('(prefers-color-scheme: dark)');

  /* A `localStorage` privát ablakban és letiltott sütiknél dobhat. A téma nem
     kritikus funkció, ezért itt a hiba elnyelése a helyes válasz: a látogató a
     rendszerbeállítást kapja, csak nem jegyezzük meg a választását. */
  const mentett = () => {
    try {
      const t = localStorage.getItem(KULCS);
      return t === 'dark' || t === 'light' ? t : null;
    } catch {
      return null;
    }
  };

  const megjegyez = (tema) => {
    try {
      localStorage.setItem(KULCS, tema);
    } catch {
      /* nem jegyezzük meg — az aktuális oldalon így is működik */
    }
  };

  const alkalmaz = (tema) => {
    gyoker.dataset.theme = tema;
  };

  alkalmaz(mentett() || (rendszerSotet.matches ? 'dark' : 'light'));

  document.addEventListener('DOMContentLoaded', () => {
    const valto = document.querySelector('[data-tema-valto]');
    if (!valto) return;
    const tipp = document.querySelector('[data-tema-tipp]');

    /* A gomb `role="switch"`: a NEVE állandó („Sötét téma"), az állapotát az
       `aria-checked` hordozza — ez a kapcsolók helyes ARIA-mintája. A lebegő
       súgó ezzel szemben a MŰVELETET mondja ki, és `aria-hidden`, hogy a
       képernyőolvasó ne olvassa fel kétszer ugyanazt. */
    const frissit = () => {
      const sotet = gyoker.dataset.theme === 'dark';
      valto.setAttribute('aria-checked', String(sotet));
      if (tipp) {
        tipp.textContent = sotet ? 'Váltás világos témára' : 'Váltás sötét témára';
      }
    };

    frissit();

    valto.addEventListener('click', () => {
      const uj = gyoker.dataset.theme === 'dark' ? 'light' : 'dark';
      alkalmaz(uj);
      megjegyez(uj);
      frissit();
    });

    /* Ha a látogató még nem választott, kövessük élőben a rendszerbeállítást —
       például amikor az operációs rendszer napnyugtakor sötétre vált. Saját
       választás után nem nyúlunk hozzá. */
    rendszerSotet.addEventListener('change', (e) => {
      if (mentett()) return;
      alkalmaz(e.matches ? 'dark' : 'light');
      frissit();
    });
  });
})();
