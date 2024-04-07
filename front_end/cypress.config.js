import { defineConfig } from "cypress";

export default defineConfig({
  projectId: 'icr9s9',
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    experimentalStudio: true,
  },
});
