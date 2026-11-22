export const productionRows=`
Multi-level BOMs|多层物料清单|多層物料清單|Nomenclatures multiniveaux
Manufacture orders|制造订单|製造訂單|Ordres de fabrication
Labor approvals|工时审批|工時核准|Approbation du travail
Legacy BOMs & work orders|原有物料清单及工单|原有物料清單及工單|Nomenclatures et ordres existants
Production cost report CSV|生产成本报表 CSV|生產成本報表 CSV|Rapport des coûts de production CSV
New production BOM|新建生产物料清单|新增生產物料清單|Nouvelle nomenclature de production
Create BOM revision|创建物料清单修订版|建立物料清單修訂版|Créer une révision
Plan manufacture order|计划制造订单|規劃製造訂單|Planifier un ordre de fabrication
Frozen BOM version|固定物料清单版本|固定物料清單版本|Version figée de la nomenclature
Quantity per finished unit|每件成品用量|每件成品用量|Quantité par unité finie
Subassembly BOM|子装配物料清单|子組裝物料清單|Nomenclature du sous-ensemble
Purchased material|外购材料|外購材料|Matière achetée
Production stages|生产工序|生產工序|Étapes de production
Work instructions|作业说明|作業說明|Instructions de travail
Estimated minutes per unit|每件预计分钟数|每件預計分鐘數|Minutes estimées par unité
Hourly costing rate|每小时成本费率|每小時成本費率|Taux horaire de coût
Estimated unit build cost|预计单位制造成本|預計單位製造成本|Coût estimé de fabrication unitaire
Estimates use current material costs. Actual costs are frozen when production starts and labor is approved.|估算使用当前材料成本。实际成本在投产及工时获批时固定。|估算使用目前材料成本。實際成本在投產及工時獲准時固定。|Les estimations utilisent les coûts actuels. Les coûts réels sont figés au démarrage et à l’approbation du travail.
BOM revision history|物料清单修订历史|物料清單修訂歷史|Historique des révisions
No production records yet.|暂无生产记录。|尚無生產記錄。|Aucun enregistrement de production.
Start work order|开始工单|開始工單|Démarrer l’ordre de travail
Receive finished goods|成品入库|成品入庫|Réceptionner les produits finis
Planned quantity|计划数量|計畫數量|Quantité prévue
Completed quantity|完工数量|完工數量|Quantité terminée
Remaining quantity|剩余数量|剩餘數量|Quantité restante
Material cost|材料成本|材料成本|Coût des matières
Approved labor cost|已批准工时成本|已核准工時成本|Coût du travail approuvé
Overhead cost|制造费用|製造費用|Frais indirects
Remaining WIP value|剩余在制品价值|剩餘在製品價值|Valeur restante des encours
Child work orders|子工单|子工單|Ordres de travail enfants
Material requirements|材料需求|材料需求|Besoins en matières
Stage result|工序结果|工序結果|Résultat de l’étape
Record labor time|记录工时|記錄工時|Saisir le temps de travail
Complete stage|完成工序|完成工序|Terminer l’étape
Labor entries|工时记录|工時記錄|Saisies de temps
Finished-goods receipts|成品入库记录|成品入庫記錄|Réceptions de produits finis
Production cost|生产成本|生產成本|Coût de production
Cancel manufacture order|取消制造订单|取消製造訂單|Annuler l’ordre de fabrication
Complete child work orders before the parent assembly. BOM revisions are frozen when the order is planned.|先完成子工单，再开始父装配。订单计划时固定物料清单版本。|先完成子工單，再開始父組裝。訂單規劃時固定物料清單版本。|Terminez les ordres enfants avant l’assemblage parent. Les versions sont figées à la planification.
Production creates separate child work orders for nested subassemblies. Complete children before starting the parent.|嵌套子装配生成独立子工单。先完成子工单，再开始父工单。|巢狀子組裝產生獨立子工單。先完成子工單，再開始父工單。|Chaque sous-ensemble possède son ordre enfant. Terminez les enfants avant de démarrer le parent.
Only approved labor enters work in progress. Manufacturing operators submit time; Accounting or Admin reviews it.|只有获批工时计入在制品。制造人员提交工时，由会计或管理员审核。|只有獲准工時計入在製品。製造人員提交工時，由會計或管理員審核。|Seul le travail approuvé entre dans les encours. La fabrication soumet le temps; la comptabilité ou l’administrateur le vérifie.
Versioned BOMs, staged production and approved labor costs. Existing documents and historical costs are preserved.|版本化物料清单、分工序生产及已批准工时成本。保留现有单据和历史成本。|版本化物料清單、分工序生產及已核准工時成本。保留現有單據和歷史成本。|Nomenclatures versionnées, étapes de production et coûts du travail approuvés. Les documents et coûts historiques sont préservés.
Hourly costing rate|每小时成本费率|每小時成本費率|Taux horaire de coût
Labor cost|工时成本|工時成本|Coût du travail
Review labor|审核工时|審核工時|Vérifier le travail
BOM component|物料清单组件|物料清單組件|Composant de nomenclature
Subassembly BOM (optional)|子装配物料清单（可选）|子組裝物料清單（選填）|Nomenclature du sous-ensemble (facultatif)
Remove component|移除组件|移除組件|Retirer le composant
Production stage|生产工序|生產工序|Étape de production
Stage name|工序名称|工序名稱|Nom de l’étape
Remove stage|移除工序|移除工序|Retirer l’étape
BOM name|物料清单名称|物料清單名稱|Nom de la nomenclature
Overhead per finished unit|每件成品制造费用|每件成品製造費用|Frais indirects par unité finie
Add component|添加组件|新增組件|Ajouter un composant
Add stage|添加工序|新增工序|Ajouter une étape
Saving creates a new version. Existing manufacture orders keep their original BOM and instructions.|保存会创建新版本。现有制造订单保留原物料清单及说明。|儲存會建立新版本。現有製造訂單保留原物料清單及說明。|L’enregistrement crée une version. Les ordres existants conservent leur nomenclature et leurs instructions.
Save BOM version|保存物料清单版本|儲存物料清單版本|Enregistrer la version
Create a production BOM first.|请先创建生产物料清单。|請先建立生產物料清單。|Créez d’abord une nomenclature de production.
Production BOM|生产物料清单|生產物料清單|Nomenclature de production
Starting consumes available materials into work in progress at their preserved cost. Child work orders must be completed first.|开始时按保留成本将可用材料转入在制品。必须先完成子工单。|開始時依保留成本將可用材料轉入在製品。必須先完成子工單。|Le démarrage transfère les matières disponibles vers les encours à leur coût préservé. Terminez d’abord les ordres enfants.
Actual minutes|实际分钟数|實際分鐘數|Minutes réelles
Labor note|工时备注|工時備註|Note de travail
Time is submitted for approval. No cost is posted until Accounting or Admin approves it.|工时提交审批。会计或管理员批准后才过账成本。|工時提交審核。會計或管理員核准後才過帳成本。|Le temps est soumis à approbation. Aucun coût n’est comptabilisé avant sa validation par la comptabilité ou l’administrateur.
Submit labor|提交工时|提交工時|Soumettre le temps
Approval reason|审批说明|核准說明|Motif de la décision
I reviewed the time entry and costing rate.|我已核对工时及成本费率。|我已確認工時及成本費率。|J’ai vérifié le temps et le taux de coût.
Save labor decision|保存工时决定|儲存工時決定|Enregistrer la décision
I reviewed the stage instructions and result.|我已核对工序说明及结果。|我已確認工序說明及結果。|J’ai vérifié les instructions et le résultat de l’étape.
Receipt location|入库库位|入庫庫位|Emplacement de réception
Finished lot|成品批次|成品批號|Lot des produits finis
Partial receipts allocate frozen material, approved labor and overhead costs. The remaining cost stays in work in progress.|部分入库分摊已固定材料、获批工时及制造费用。剩余成本保留在在制品中。|部分入庫分攤已固定材料、獲准工時及製造費用。剩餘成本保留在在製品中。|Les réceptions partielles répartissent les coûts figés des matières, du travail approuvé et des frais indirects. Le solde reste dans les encours.
Production record saved.|生产记录已保存。|生產記錄已儲存。|Enregistrement de production sauvegardé.
Private staging · production editable|私人测试 · 可编辑生产|私人測試 · 可編輯生產|Test privé · production modifiable
Cloud staging · production editable|云端测试 · 可编辑生产|雲端測試 · 可編輯生產|Test cloud · production modifiable
Manufacturing changes are saved separately from the preserved import. Other operations remain read-only.|制造更改单独保存，保留原始导入数据。其他操作仍为只读。|製造變更分開儲存，保留原始匯入資料。其他操作仍為唯讀。|Les modifications de fabrication sont enregistrées séparément de l’import préservé. Les autres opérations restent en lecture seule.
Complete child work orders before starting this work order.|请先完成子工单，再开始此工单。|請先完成子工單，再開始此工單。|Terminez les ordres enfants avant de démarrer cet ordre.
Production materials are short or reserved.|生产材料不足或已预留。|生產材料不足或已預留。|Les matières sont insuffisantes ou réservées.
Set known positive material costs before production.|请先设置已知的正数材料成本，再开始生产。|請先設定已知的正數材料成本，再開始生產。|Définissez des coûts de matières connus et positifs avant la production.
Submit labor before the first finished-goods receipt.|请在首次成品入库前提交工时。|請在首次成品入庫前提交工時。|Soumettez le travail avant la première réception de produits finis.
Labor must belong to the active production stage.|工时必须属于当前生产工序。|工時必須屬於目前生產工序。|Le travail doit concerner l’étape active.
Approve or reject submitted labor before completing the stage.|完成工序前，请批准或拒绝已提交的工时。|完成工序前，請核准或拒絕已提交的工時。|Approuvez ou refusez le travail soumis avant de terminer l’étape.
Complete all stages and resolve submitted labor before receiving finished goods.|成品入库前，请完成所有工序并处理待审批工时。|成品入庫前，請完成所有工序並處理待核准工時。|Terminez toutes les étapes et traitez le travail soumis avant la réception.
Your role cannot perform this production action.|您的角色无权执行此生产操作。|您的角色無權執行此生產操作。|Votre rôle ne permet pas cette action de production.
Production-consumed materials need a reviewed cost correction before late price or freight allocations.|已用于生产的材料需要经过审核的成本更正，才能分摊后续价差或运费。|已用於生產的材料需要經過審核的成本更正，才能分攤後續價差或運費。|Les matières consommées nécessitent une correction de coût vérifiée avant toute affectation tardive de prix ou de transport.
Staged production currently supports lot-tracked products.|分工序生产目前支持批次追踪产品。|分工序生產目前支援批號追蹤產品。|La production par étapes prend actuellement en charge le suivi par lot.
Activity history capacity reached. Export and review before continuing.|活动历史容量已满。请导出并审核后继续。|活動歷史容量已滿。請匯出並審核後繼續。|L’historique est plein. Exportez-le et vérifiez-le avant de continuer.
Enter valid production text within the allowed length.|请输入长度范围内的有效生产文本。|請輸入長度範圍內的有效生產文字。|Saisissez un texte de production valide de longueur autorisée.
Enter a valid whole production quantity or number.|请输入有效的生产整数数量。|請輸入有效的生產整數數量。|Saisissez une quantité ou un nombre entier valide.
Use a nonnegative production amount with at most two decimals.|请输入非负金额，最多两位小数。|請輸入非負金額，最多兩位小數。|Utilisez un montant positif ou nul avec deux décimales au maximum.
Use a valid production date.|请选择有效生产日期。|請選擇有效生產日期。|Utilisez une date de production valide.
Production record not found.|未找到生产记录。|找不到生產記錄。|Enregistrement de production introuvable.
Production work order not found.|未找到生产工单。|找不到生產工單。|Ordre de travail de production introuvable.
Production journal must balance.|生产日记账借贷必须平衡。|生產日記帳借貸必須平衡。|L’écriture de production doit être équilibrée.
Choose one to thirty distinct BOM components.|请选择一至三十种不同组件。|請選擇一至三十種不同組件。|Choisissez de un à trente composants distincts.
A production BOM cannot consume its own output.|物料清单不能消耗自身成品。|物料清單不能消耗自身成品。|Une nomenclature ne peut pas consommer son propre produit.
The subassembly BOM must produce the selected component.|子装配物料清单必须产出所选组件。|子組裝物料清單必須產出所選組件。|La nomenclature du sous-ensemble doit produire le composant choisi.
Add one to twelve production stages.|请添加一至十二个生产工序。|請新增一至十二個生產工序。|Ajoutez de une à douze étapes de production.
Production BOM cycles or more than eight levels are not allowed.|不允许物料清单循环引用或超过八层。|不允許物料清單循環引用或超過八層。|Les cycles et les nomenclatures de plus de huit niveaux sont interdits.
A manufacture order supports up to one hundred work orders.|每个制造订单最多包含一百个工单。|每個製造訂單最多包含一百個工單。|Un ordre de fabrication accepte cent ordres de travail au maximum.
Unknown production action.|未知生产操作。|未知生產操作。|Action de production inconnue.
A BOM revision must keep the same finished product.|修订版必须保留同一成品。|修訂版必須保留同一成品。|Une révision doit conserver le même produit fini.
Production cost is outside the allowed range.|生产成本超出允许范围。|生產成本超出允許範圍。|Le coût de production dépasse la plage autorisée.
Only an entirely unstarted manufacture order can be cancelled.|只能取消所有工单均未开始的制造订单。|只能取消所有工單均未開始的製造訂單。|Seul un ordre de fabrication entièrement non démarré peut être annulé.
The manufacture order is cancelled.|制造订单已取消。|製造訂單已取消。|L’ordre de fabrication est annulé.
Production stock changed; refresh and review.|生产库存已更改；请刷新并审核。|生產庫存已變更；請重新整理並審核。|Le stock de production a changé. Actualisez et vérifiez.
Enter a positive hourly costing rate.|请输入大于零的每小时成本费率。|請輸入大於零的每小時成本費率。|Saisissez un taux horaire de coût positif.
Labor cost is outside the allowed range.|工时成本超出允许范围。|工時成本超出允許範圍。|Le coût du travail dépasse la plage autorisée.
Choose a submitted time entry on the active stage.|请选择当前工序已提交的工时。|請選擇目前工序已提交的工時。|Choisissez une saisie soumise pour l’étape active.
Review the labor approval decision.|请审核工时审批决定。|請審核工時核准決定。|Vérifiez la décision d’approbation du travail.
Complete the active production stage in sequence.|请依次完成当前生产工序。|請依序完成目前生產工序。|Terminez l’étape active dans l’ordre.
Review the stage instructions and result.|请核对工序说明及结果。|請確認工序說明及結果。|Vérifiez les instructions et le résultat de l’étape.
Choose an owned receipt location in the manufacture order warehouse.|请选择制造订单仓库内自有库存的入库库位。|請選擇製造訂單倉庫內自有庫存的入庫庫位。|Choisissez un emplacement de réception en propriété dans l’entrepôt de l’ordre.
Finished goods need a positive production cost.|成品生产成本必须大于零。|成品生產成本必須大於零。|Le coût de production des produits finis doit être positif.
Set an opening output cost before mixing existing inventory.|与现有库存混合前，请设置成品期初成本。|與現有庫存混合前，請設定成品期初成本。|Définissez un coût initial du produit avant de le mélanger au stock existant.
Component|组件|組件|Composant
Version|版本|版本|Version
BOM|物料清单|物料清單|Nomenclature
Components|组件|組件|Composants
Planned|已计划|已規劃|Planifié
In progress|进行中|進行中|En cours
Required|需求数量|需求數量|Quantité requise
Short|短缺数量|短缺數量|Quantité manquante
Work order|工单|工單|Ordre de travail
Manufacture order|制造订单|製造訂單|Ordre de fabrication
Work orders|工单|工單|Ordres de travail
Minutes|分钟|分鐘|Minutes
Submitted|已提交|已提交|Soumis
Decision|决定|決定|Décision
Material cents|材料成本（分）|材料成本（分）|Matières en cents
Approved labor cents|已批准工时成本（分）|已核准工時成本（分）|Travail approuvé en cents
Overhead cents|制造费用（分）|製造費用（分）|Frais indirects en cents
WIP cents|在制品成本（分）|在製品成本（分）|Encours en cents
Invalid production ledger.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid or duplicate production identity.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid BOM version history.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid BOM revision identity.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
BOM revision content changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Production journal source changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid manufacture order.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Manufacture order work tree changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Frozen work order BOM changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid work-order dependency.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Frozen production stage changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Production stages must finish in sequence.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Only one production stage can be active.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid production completion balance.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Production material quantities or dependencies changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Production material journal amount changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Production consumption source changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Missing FIFO production consumption.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Unstarted production cannot have costs or receipts.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Partial completion costs changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Finished goods WIP journal changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
A completion needs finished stages.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
FIFO completion receipt changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Completed work order has a remaining quantity.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Completed quantity needs completed status.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Production WIP cannot be negative.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Manufacture order status changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Invalid production labor entry.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Labor approval evidence is missing.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Approved labor journal changed.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Unapproved labor cannot post a cost.|生产记录校验未通过。请刷新并联系管理员。|生產記錄驗證未通過。請重新整理並聯絡管理員。|La validation des enregistrements de production a échoué. Actualisez et contactez l’administrateur.
Issued quantity|已领料数量|已領料數量|Quantité sortie
Manufacturing edits use a separate saved workspace. CRM permissions are unchanged; other operations remain read-only.|制造更改保存在独立工作区。CRM 权限不变；其他操作仍为只读。|製造變更儲存在獨立工作區。CRM 權限不變；其他操作仍為唯讀。|Les modifications de fabrication sont enregistrées séparément. Les droits CRM sont conservés; les autres opérations restent en lecture seule.
Assembly|装配|組裝|Assemblage
Inspection|检验|檢驗|Contrôle
Packaging|包装|包裝|Emballage
Check components and assemble to the work instructions.|核对组件，按说明装配。|核對組件，依說明組裝。|Vérifiez les composants et assemblez-les conformément aux instructions.
Check quantity and appearance.|检查数量和外观。|檢查數量及外觀。|Vérifiez la quantité et l’aspect.
Confirm the lot and pack the output.|确认批次并包装。|確認批號後包裝。|Confirmez le lot et emballez le produit.
Demo checks passed|示例检查通过|範例檢查通過|Contrôles de démonstration réussis
Verified demo minutes and costing rate|已核对工时和费率|已確認工時及費率|Minutes et taux de coût de démonstration vérifiés
Needs attention|需关注|需關注|Points à surveiller
Status colors|状态颜色|狀態顏色|Couleurs des statuts
Not started|未开始|未開始|Non démarré
Complete or ready|已完成或可开始|已完成或可開始|Terminé ou prêt
Waiting for action|等待处理|等待處理|Action en attente
Needs review|需要审核|需要審核|À vérifier
No action needed|无需处理|無需處理|Aucune action requise
Ready to start|可以开始|可以開始|Prêt à démarrer
Continue active stage|继续当前工序|繼續目前工序|Poursuivre l’étape active
Waiting for child work|等待子工单|等待子工單|En attente des ordres enfants
Material shortage|材料短缺|材料短缺|Matières insuffisantes
Material cost missing|缺少材料成本|缺少材料成本|Coût des matières manquant
Labor awaiting approval|工时待审批|工時待核准|Travail en attente d’approbation
Rejected labor needs review|被拒绝的工时需复核|被拒絕的工時需覆核|Travail refusé à vérifier
Ready to receive finished goods|可以接收成品|可以接收成品|Produits finis à réceptionner
Finish remaining receipt|请完成剩余入库|請完成剩餘入庫|Terminer la réception restante
Start work order first|请先开始工单|請先開始工單|Démarrer d’abord l’ordre de travail
Waiting for earlier stage|等待前一道工序|等待前一道工序|En attente de l’étape précédente
Material planning|制造物料计划|製造物料計劃|Planification des matières
Production schedule|生产排程|生產排程|Planning de production
Manufacturing planning saved|制造计划已保存|製造計劃已儲存|Planification de fabrication enregistrée
Planning filters|计划筛选|計劃篩選|Filtres de planification
Export planning CSV|导出计划 CSV|匯出計劃 CSV|Exporter la planification CSV
Planning does not reserve stock or post costs. Purchase drafts require separate approval.|计划不会预留库存或记入成本。采购草稿需要单独审批。|計劃不會預留庫存或入賬成本。採購草稿需要另外核准。|La planification ne réserve pas de stock et ne comptabilise aucun coût. Les brouillons d’achat nécessitent une approbation distincte.
Material requirements by work order|按工单查看物料需求|按工單檢視物料需求|Besoins en matières par ordre de travail
Manufacture order / Work order|制造订单 / 工单|製造訂單 / 工單|Ordre de fabrication / travail
Required by|需求日期|需求日期|Requis pour le
Required quantity|需求数量|需求數量|Quantité requise
Allocated stock|已分配库存|已分配庫存|Stock affecté
Timely purchase supply|按时到货采购|按時到貨採購|Achats attendus à temps
Planned production supply|计划生产供应|計劃生產供應|Approvisionnement de production prévu
Short quantity|短缺数量|短缺數量|Quantité manquante
Late or uncertain supply|延迟或日期未定供应|延遲或日期未定供應|Approvisionnement tardif ou incertain
Only unstarted work consumes planning demand. Dated supply is allocated once, in required-date order. Expected production is available the day after its scheduled finish.|仅未开工工单计入物料需求。按需求日期依次分配供应，避免重复计算。预计产出于排程完成次日可用。|只有未開工工單計入物料需求。按需求日期依次分配供應，避免重複計算。預計產出於排程完成翌日可用。|Seuls les travaux non démarrés génèrent des besoins. Chaque approvisionnement est affecté une seule fois, par date requise. La production prévue est disponible le lendemain de sa fin planifiée.
Material purchase proposals|物料采购建议|物料採購建議|Propositions d’achat de matières
Unissued purchase quantity|未下达采购数量|未發出採購數量|Quantité d’achats non émis
Proposed quantity|已建议数量|已建議數量|Quantité proposée
Suggested purchase quantity|建议采购数量|建議採購數量|Quantité d’achat suggérée
Order by|最晚下单日期|最遲下單日期|Commander avant le
Lead time risk|交期风险|交期風險|Risque de délai
Review material proposal|审核物料建议|審核物料建議|Examiner la proposition de matières
Review existing proposals|查看现有建议|檢視現有建議|Examiner les propositions existantes
Unissued purchases and proposals prevent duplicate buying but are not available material supply. Subassembly shortages require child work, not automatic purchasing.|未下达采购和采购建议用于避免重复采购，但不视为可用物料。子组件短缺需要子工单生产，不会自动采购。|未發出採購和採購建議用於避免重複採購，但不視為可用物料。子組件短缺需要子工單生產，不會自動採購。|Les achats non émis et propositions évitent les doublons sans constituer un stock disponible. Les sous-ensembles manquants nécessitent des travaux enfants et ne sont pas achetés automatiquement.
Saved material proposals|已保存物料建议|已儲存物料建議|Propositions de matières enregistrées
Proposal|建议单|建議單|Proposition
Linked purchase|关联采购订单|關聯採購訂單|Achat lié
Create linked purchase draft|创建关联采购草稿|建立關聯採購草稿|Créer un brouillon d’achat lié
Cancel proposal|取消建议|取消建議|Annuler la proposition
Converted|已转采购|已轉採購|Convertie
New work center|新增工作中心|新增工作中心|Nouveau poste de travail
Schedule work order|安排工单|安排工單|Planifier l’ordre de travail
Work centers|工作中心|工作中心|Postes de travail
Work center|工作中心|工作中心|Poste de travail
Daily capacity minutes|每日产能分钟数|每日產能分鐘數|Capacité quotidienne en minutes
Working days|工作日|工作日|Jours ouvrés
Edit work center|编辑工作中心|編輯工作中心|Modifier le poste de travail
Open work schedule|未完成工单排程|未完成工單排程|Planning des travaux ouverts
Remaining estimated minutes|剩余预计分钟数|剩餘預計分鐘數|Minutes estimées restantes
Scheduled start|计划开始日期|計劃開始日期|Début planifié
Scheduled finish|计划结束日期|計劃結束日期|Fin planifiée
Edit schedule|修改排程|修改排程|Modifier le planning
Remove schedule|移除排程|移除排程|Retirer du planning
Daily work-center load|每日工作中心负荷|每日工作中心負荷|Charge quotidienne des postes
Scheduled minutes|已安排分钟数|已安排分鐘數|Minutes planifiées
Capacity minutes|产能分钟数|產能分鐘數|Capacité en minutes
Overload minutes|超负荷分钟数|超負荷分鐘數|Minutes de surcharge
Load|负荷|負荷|Charge
Capacity exceeded|超过产能|超出產能|Capacité dépassée
Within capacity|产能范围内|產能範圍內|Dans la capacité
Nonworking day|非工作日|非工作日|Jour non ouvré
Unscheduled|尚未排程|尚未排程|Non planifié
Scheduled|已排程|已排程|Planifié
Finishes after due date|结束晚于交期|結束晚於交期|Fin après l’échéance
Child work is unscheduled|子工单尚未排程|子工單尚未排程|Travaux enfants non planifiés
Child schedule overlaps parent|子工单与父工单排程重叠|子工單與父工單排程重疊|Chevauchement parent-enfant
Minutes are spread evenly across working days in each booking. Finished stages release their estimated load. Scheduling is advisory; review material availability before starting work.|每个排程的分钟数平均分配到工作日。已完成工序释放预计负荷。排程仅作规划，开工前须审核物料供应。|每個排程的分鐘數平均分配到工作日。已完成工序釋放預計負荷。排程僅作規劃，開工前須審核物料供應。|Les minutes sont réparties sur les jours ouvrés. Les étapes terminées libèrent leur charge estimée. Le planning est indicatif ; vérifiez les matières avant de démarrer.
Plan material demand, review purchase proposals and schedule production without rewriting historical costs.|规划物料需求、审核采购建议和安排生产，不改写历史成本。|規劃物料需求、審核採購建議和安排生產，不改寫歷史成本。|Planifiez les matières, examinez les achats proposés et organisez la production sans modifier les coûts historiques.
Schedule from|排程起始日期|排程起始日期|Planning à partir du
Schedule days|排程天数|排程天數|Nombre de jours du planning
Work-center code|工作中心代码|工作中心代碼|Code du poste de travail
Work-center name|工作中心名称|工作中心名稱|Nom du poste de travail
Working days (0=Sunday, 6=Saturday)|工作日（0=星期日，6=星期六）|工作日（0=星期日，6=星期六）|Jours ouvrés (0=dimanche, 6=samedi)
Save work center|保存工作中心|儲存工作中心|Enregistrer le poste de travail
Planning note|计划备注|計劃備註|Note de planification
I reviewed capacity, materials and child-work dependencies.|我已审核产能、物料和子工单依赖。|我已審核產能、物料和子工單相依關係。|J’ai vérifié la capacité, les matières et les dépendances des travaux enfants.
Capacity overloads remain visible for review. Child work must be scheduled before its parent.|超负荷会显示供审核。子工单须安排在父工单之前。|超負荷會顯示供審核。子工單須安排在父工單之前。|Les surcharges restent visibles pour examen. Les travaux enfants doivent précéder leur parent.
Save schedule|保存排程|儲存排程|Enregistrer le planning
I reviewed material demand, incoming supply and purchase packs.|我已审核物料需求、到货供应和采购包装。|我已審核物料需求、到貨供應和採購包裝。|J’ai vérifié les besoins, les arrivages et les conditionnements d’achat.
Creates a proposal only. No purchase is issued and no cost is posted.|仅创建建议单，不下达采购或记入成本。|只建立建議單，不發出採購或入賬成本。|Crée uniquement une proposition, sans émission d’achat ni comptabilisation de coût.
Save material proposal|保存物料建议|儲存物料建議|Enregistrer la proposition de matières
Administrator review is required. This creates an unissued purchase draft; purchasing approval and issue remain separate.|需要管理员审核。此操作创建未下达采购草稿；采购审批和下达为独立步骤。|需要管理員審核。此操作建立未發出採購草稿；採購核准和發出為獨立步驟。|L’examen d’un administrateur est requis. Un brouillon d’achat non émis est créé ; son approbation et son émission sont des étapes distinctes.
Reviewed price per stock unit|已审核每库存单位价格|已審核每庫存單位價格|Prix vérifié par unité de stock
Expected arrival date|预计到货日期|預計到貨日期|Date d’arrivée prévue
I reviewed supplier, quantity, price and arrival date.|我已审核供应商、数量、价格和到货日期。|我已審核供應商、數量、價格和到貨日期。|J’ai vérifié le fournisseur, la quantité, le prix et la date d’arrivée.
Planning record not found.|未找到计划记录。|找不到計劃記錄。|Enregistrement de planification introuvable.
Enter valid planning text within the field limit.|请输入长度范围内的有效计划文字。|請輸入長度限制內的有效計劃文字。|Saisissez un texte valide dans la limite autorisée.
Enter a valid whole planning number.|请输入有效的计划整数。|請輸入有效的計劃整數。|Saisissez un nombre entier de planification valide.
Planning history capacity reached.|计划历史记录容量已满。|計劃歷程記錄容量已滿。|La capacité de l’historique de planification est atteinte.
Schedule a range of at most 366 days.|排程范围最多为366天。|排程範圍最多為366天。|La période planifiée ne peut pas dépasser 366 jours.
Your role cannot perform this planning action.|您的角色无权执行此计划操作。|您的角色無權執行此計劃操作。|Votre rôle ne permet pas cette action de planification.
Use a unique work-center code and name.|请填写唯一的工作中心代码和名称。|請填寫唯一的工作中心代碼和名稱。|Indiquez un code unique et un nom de poste de travail.
Choose valid working days.|请选择有效工作日。|請選擇有效工作日。|Choisissez des jours ouvrés valides.
A scheduled work center cannot change warehouse.|已有排程的工作中心不能更换仓库。|已有排程的工作中心不能更換倉庫。|Un poste déjà planifié ne peut pas changer d’entrepôt.
Schedule an open work order with remaining estimated minutes.|请安排仍有预计工时的未完成工单。|請安排仍有預計工時的未完成工單。|Planifiez un ordre ouvert avec des minutes estimées restantes.
Choose a work center in the work order warehouse.|请选择工单所在仓库的工作中心。|請選擇工單所在倉庫的工作中心。|Choisissez un poste dans l’entrepôt de l’ordre de travail.
Schedule today or a future date.|请选择今天或以后的排程日期。|請選擇今天或之後的排程日期。|Planifiez à partir d’aujourd’hui ou d’une date future.
The date range has no working days.|此日期范围内没有工作日。|此日期範圍內沒有工作日。|Cette période ne contient aucun jour ouvré.
Schedule child work to finish before the parent start date.|请安排子工单在父工单开始前完成。|請安排子工單在父工單開始前完成。|Planifiez la fin des travaux enfants avant le début du parent.
Child work must finish before the scheduled parent starts.|子工单必须在已安排的父工单开始前完成。|子工單必須在已安排的父工單開始前完成。|Les travaux enfants doivent finir avant le début planifié du parent.
Review capacity, materials and dependencies before scheduling.|排程前请审核产能、物料和依赖关系。|排程前請審核產能、物料和相依關係。|Vérifiez la capacité, les matières et les dépendances avant de planifier.
Only open work can be unscheduled.|只能移除未完成工单的排程。|只能移除未完成工單的排程。|Seuls les travaux ouverts peuvent être retirés du planning.
Enter a reason for removing the schedule.|请输入移除排程的原因。|請輸入移除排程的原因。|Indiquez la raison du retrait du planning.
Recalculate today and review the material proposal.|请按今天日期重新计算并审核物料建议。|請按今天日期重新計算並審核物料建議。|Recalculez à la date du jour et examinez la proposition.
Material demand or supply changed. Recalculate before proposing.|物料需求或供应已变化，请重新计算再创建建议。|物料需求或供應已變更，請重新計算再建立建議。|Les besoins ou approvisionnements ont changé. Recalculez avant de proposer.
Cancel only an unconverted proposal with a reason.|只能取消未转采购的建议，并须填写原因。|只能取消未轉採購的建議，並須填寫原因。|Annulez uniquement une proposition non convertie, avec un motif.
Review an unconverted material proposal.|请审核尚未转采购的物料建议。|請審核尚未轉採購的物料建議。|Examinez une proposition de matières non convertie.
Material demand or supply changed. Cancel and recreate the proposal.|物料需求或供应已变化，请取消并重新创建建议。|物料需求或供應已變更，請取消並重新建立建議。|Les besoins ou approvisionnements ont changé. Annulez et recréez la proposition.
Review a positive unit price with up to four decimals.|请审核大于零且最多四位小数的单价。|請審核大於零且最多四位小數的單價。|Vérifiez un prix unitaire positif avec quatre décimales au maximum.
Choose today or a future purchase arrival date.|请选择今天或以后的采购到货日期。|請選擇今天或之後的採購到貨日期。|Choisissez une arrivée d’achat à partir d’aujourd’hui.
Recalculate the material plan.|请重新计算物料计划。|請重新計算物料計劃。|Recalculez le plan des matières.
Material readiness|物料就绪情况|物料就緒情況|Disponibilité des matières
Materials issued|物料已发出|物料已發出|Matières sorties
Materials expected|等待预计供应|等待預計供應|Matières attendues
Materials available|物料可用|物料可用|Matières disponibles
Purchase packs changed. Recreate the proposal.|采购包装已变更，请重新创建建议。|採購包裝已變更，請重新建立建議。|Le conditionnement d’achat a changé. Recréez la proposition.
`;

