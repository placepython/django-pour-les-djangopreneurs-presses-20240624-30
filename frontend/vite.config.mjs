import { defineConfig } from "vite";
import path from "path";
import { glob } from "glob";

const PROJECT_ROOT = "../";

/**
 * Returns an objet for vite rollup$Options input
 */
function getInputFiles(pattern) {
  return glob.sync(pattern).reduce((entries, file) => {
    const entry = path.relative(PROJECT_ROOT, file);
    entries[entry] = file;
    return entries;
  }, {});
}

function setOutputFiles(folder) {
  return (assetInfo) => {
    const extname = path.extname(assetInfo.name);
    const name = path.basename(assetInfo.name, extname);
    return `${folder}/${name}-[hash]${extname}`;
  };
}

// Collection of input files
const input = {
  ...getInputFiles("src/application/**/*.{js,ts}"),
  ...getInputFiles("src/styles/*.{css,scss}"),
};

// Definition of output files
const output = {
  entryFileNames: setOutputFiles("assets"),
  assetFileNames: setOutputFiles("assets"),
};

// Configuration entry point
export default defineConfig({
  plugins: [],
  base: "/static/",
  server: {
    open: false,
  },
  build: {
    manifest: "manifest.json",
    emptyOutDir: true,
    rollupOptions: {
      input,
      output,
    },
  },
});
