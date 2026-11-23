import {roleCommands,commandRoleAllowed} from './command-policy.mjs?demo=45f52980507d3a1b';
import {inventoryCommands} from './inventory-policy.mjs?demo=45f52980507d3a1b';
// The full cloud transaction path is opt-in per tenant. It never exposes
// workspace replacement/reset, user administration, synthetic seeds or QBO send.
const excluded=new Set(['removeCarton','receiving:loadDemo']);
const allowed=c=>!c.startsWith('crm:')&&!c.startsWith('production:')&&!excluded.has(c);
const administrative=[
 'createLocation','importCatalog','saveCustom','createItem','saveItemText','setTracking',
 'business:owner','business:warehouse','business:location','business:profile',
 'business:price','business:vendorPrice','business:applyVendorPrices','business:kit',
 'business:bom','business:work','business:customer','business:purchase','business:sale',
 'proc:policy','proc:approve','proc:reject','count:approve','voidPick','voidShipment','deleteCarton'
];
export const operationalCommands=Object.freeze([...new Set([...Object.values(roleCommands).flat(),...inventoryCommands,...administrative].filter(allowed))].sort());
export const operationalRoleAllowed=(command,role)=>operationalCommands.includes(command)&&commandRoleAllowed(command,role);
export const operationalAllowed=role=>operationalCommands.filter(command=>operationalRoleAllowed(command,role));
