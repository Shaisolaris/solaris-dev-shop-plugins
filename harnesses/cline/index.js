import { createTool } from '@cline/sdk';
import { intake, schema } from './native/intake.mjs';

export default {
  name: 'solaris-dev-shop',
  manifest: { capabilities: ['tools'] },
  setup(api) {
    api.registerTool(createTool({
      name: 'solaris_intake',
      description: 'Classify a request through the pinned local Solaris coordinator. Returns an assignment; executes no specialist work.',
      inputSchema: schema,
      execute: intake,
    }));
  },
};
