/**
 * formatSchemaDate — ISO 8601 completo con offset America/Santiago.
 * Uso en generadores / inyección de JSON-LD. No inventar fechas: pasar la fecha real.
 *
 * @param {string|Date} input  Fecha (YYYY-MM-DD, ISO parcial, o Date)
 * @param {string} [time='12:00:00'] Hora local Chile si solo hay fecha
 * @returns {string} ej. "2026-09-04T12:00:00-04:00"
 */
(function (root) {
  function pad(n) { return String(n).padStart(2, '0'); }

  function offsetForChile(date) {
    // America/Santiago via Intl (maneja DST histórico)
    try {
      var parts = new Intl.DateTimeFormat('en-US', {
        timeZone: 'America/Santiago',
        timeZoneName: 'shortOffset',
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false
      }).formatToParts(date);
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var tz = map.timeZoneName || 'GMT-4';
      var m = tz.match(/GMT([+-])(\d+)(?::?(\d+))?/);
      if (m) {
        return m[1] + pad(m[2]) + ':' + pad(m[3] || '0');
      }
    } catch (e) { /* fallthrough */ }
    return '-04:00';
  }

  function formatSchemaDate(input, time) {
    time = time || '12:00:00';
    var y, mo, d, h, mi, s;

    if (input instanceof Date) {
      // Interpret absolute instant → wall clock in Chile
      var fmt = new Intl.DateTimeFormat('en-CA', {
        timeZone: 'America/Santiago',
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false
      });
      var parts = fmt.formatToParts(input);
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      y = map.year; mo = map.month; d = map.day;
      h = map.hour === '24' ? '00' : map.hour;
      mi = map.minute; s = map.second;
      var localAsUtc = new Date(Date.UTC(+y, +mo - 1, +d, +h, +mi, +s));
      return y + '-' + mo + '-' + d + 'T' + h + ':' + mi + ':' + s + offsetForChile(localAsUtc);
    }

    var str = String(input).trim();
    // Already has offset or Z → normalize only if date-only missing time
    if (/^\d{4}-\d{2}-\d{2}T/.test(str) && /([+-]\d{2}:\d{2}|Z)$/.test(str)) {
      return str.replace(/Z$/, '+00:00');
    }

    var dm = str.match(/^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?/);
    if (!dm) throw new Error('formatSchemaDate: invalid date ' + str);
    y = dm[1]; mo = dm[2]; d = dm[3];
    if (dm[4] != null) {
      h = dm[4]; mi = dm[5]; s = dm[6] || '00';
    } else {
      var tm = time.split(':');
      h = pad(tm[0]); mi = pad(tm[1] || '0'); s = pad(tm[2] || '0');
    }
    // Build a Date approximating that Chile wall time for offset lookup
    var probe = new Date(Date.UTC(+y, +mo - 1, +d, +h, +mi, +s));
    return y + '-' + mo + '-' + d + 'T' + h + ':' + mi + ':' + s + offsetForChile(probe);
  }

  root.formatSchemaDate = formatSchemaDate;
  if (typeof module !== 'undefined' && module.exports) module.exports = { formatSchemaDate: formatSchemaDate };
})(typeof globalThis !== 'undefined' ? globalThis : this);
