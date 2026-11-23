// The native maximum caps Chrome's year entry at four digits.
export const dateInputBounds=type=>type==='date'?'min="0001-01-01" max="9999-12-31"':type==='datetime-local'?'min="0001-01-01T00:00" max="9999-12-31T23:59:59"':'';
