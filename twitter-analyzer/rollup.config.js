import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';

export default {
  input: 'src/view.js',
  output: {
    dir: 'dest',
    format: 'iife'
  },
  plugins: [
    resolve({
      mainFields: ['browser', 'module', 'main'],
    }), 
    commonjs(), 
    json({compact: true})
  ],
};