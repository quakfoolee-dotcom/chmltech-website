// Shared command policy has no engine imports so cold cloud entrypoints stay acyclic.
export const planningCommands=['production:center','production:schedule','production:unschedule','production:propose','production:cancelProposal','production:purchaseDraft'];
export const productionRoleAllowed=(command,role='Admin')=>command==='production:purchaseDraft'?role==='Admin':command==='production:approve'?['Admin','Accounting'].includes(role):['Admin','Manufacturing'].includes(role);

// Browser actions use the same command roles as the transactional backend.
export const productionActionCommands=Object.freeze({
 'prod-bom':'production:bom','prod-add-component':'production:bom','prod-remove-component':'production:bom','prod-add-stage':'production:bom','prod-remove-stage':'production:bom',
 'prod-plan':'production:plan','prod-start':'production:start','prod-stage':'production:stage','prod-labor':'production:labor','prod-approve':'production:approve','prod-complete':'production:complete','prod-cancel':'production:cancel',
 'prod-center':'production:center','prod-schedule':'production:schedule','prod-unschedule':'production:unschedule','prod-mrp-propose':'production:propose','prod-mrp-cancel':'production:cancelProposal','prod-mrp-purchase':'production:purchaseDraft'
});
export const productionActionAllowed=(action,role)=>Object.hasOwn(productionActionCommands,action)&&typeof role==='string'&&productionRoleAllowed(productionActionCommands[action],role);

