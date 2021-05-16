import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';

export default {
  input: 'src/view.js',
  output: {
    dir: 'dest',
    format: 'cjs'
  },
  plugins: [resolve(), commonjs(), json({compact: true})],
};