export const extraRows=`
Full database backups|完整数据库备份|完整資料庫備份|Sauvegardes complètes de la base
Create full backup|创建完整备份|建立完整備份|Créer une sauvegarde complète
Workspace JSON exports do not include accounts or QuickBooks credentials.|工作区 JSON 导出不包含账户或 QuickBooks 凭证。|工作區 JSON 匯出不包含帳戶或 QuickBooks 憑證。|Les exports JSON de l’espace ne contiennent ni comptes ni identifiants QuickBooks.
Verified full backups run at startup and hourly while Harbor is running. The latest 24 are retained.|Harbor 启动时及运行期间每小时执行已验证的完整备份，保留最近 24 份。|Harbor 啟動時及執行期間每小時執行已驗證的完整備份，保留最近 24 份。|Les sauvegardes complètes vérifiées sont créées au démarrage puis chaque heure pendant le fonctionnement de Harbor. Les 24 dernières sont conservées.
Full backup folders include the application, all database tables and the phone address. External phone certificates and Windows account encryption keys are not included.|完整备份文件夹包含应用程序、所有数据库表及手机访问地址。不包含外部手机证书及 Windows 账户加密密钥。|完整備份資料夾包含應用程式、所有資料庫表及手機存取位址。不包含外部手機憑證及 Windows 帳戶加密金鑰。|Les dossiers complets contiennent l’application, toutes les tables et l’adresse mobile. Les certificats externes et les clés du compte Windows sont exclus.
Full backup folders are saved under data/full-backups. Copy the entire folder to your private backup location.|完整备份保存在 data/full-backups。请将整个文件夹复制到您的私人备份位置。|完整備份儲存於 data/full-backups。請將整個資料夾複製到您的私人備份位置。|Les sauvegardes complètes se trouvent dans data/full-backups. Copiez le dossier entier vers votre emplacement privé de sauvegarde.
Manifest|备份清单|備份清單|Manifeste
Database snapshot|数据库快照|資料庫快照|Instantané de la base
Access|访问权限|存取權限|Accès
real|实际记录|實際記錄|données réelles
Dashboard views|仪表板视图|儀表板檢視|Vues du tableau de bord
Dashboard gadgets|仪表板小组件|儀表板小工具|Composants du tableau de bord
Warehouse overview|仓库概览|倉庫概覽|Vue d’ensemble de l’entrepôt
This quarter|本季度|本季|Ce trimestre
Last quarter|上季度|上季|Trimestre précédent
This financial year|本财年|本會計年度|Cet exercice
Last financial year|上财年|上會計年度|Exercice précédent
Last 60 days|最近 60 天|最近 60 天|60 derniers jours
Last 180 days|最近 180 天|最近 180 天|180 derniers jours
Last 365 days|最近 365 天|最近 365 天|365 derniers jours
Previous period|上一期间|上一期間|Période précédente
All categories|所有类别|所有類別|Toutes les catégories
All customers|所有客户|所有客戶|Tous les clients
All groups|所有组|所有群組|Tous les groupes
All salespeople|所有销售员|所有業務員|Tous les vendeurs
All margins|所有毛利|所有毛利|Toutes les marges
Distinct orders with issued invoices in this period; drafts and cancellations excluded.|本期间已开立发票的独立订单数；不含草稿和已取消订单。|本期間已開立發票的獨立訂單數；不含草稿和已取消訂單。|Commandes distinctes avec factures émises dans cette période; brouillons et annulations exclus.
Net invoiced units, reduced by issued customer credits. Different units are counted as base units.|净开票数量，扣除已开客户贷项。不同计量单位按基本单位计数。|淨開票數量，扣除已開客戶貸項。不同計量單位按基本單位計數。|Unités facturées nettes, diminuées des crédits clients émis. Les unités différentes sont comptées en unités de base.
Net revenue after discounts and credits, excluding tax, divided by invoiced order count. Margin uses stored shipment costs.|扣除折扣及贷项后的未税净收入除以已开票订单数。毛利使用已保存的发货成本。|扣除折扣及貸項後的未稅淨收入除以已開票訂單數。毛利使用已保存的出貨成本。|Chiffre d’affaires net après remises et crédits, hors taxes, divisé par les commandes facturées. La marge utilise les coûts d’expédition conservés.
Issued home-currency invoice net amounts minus issued customer credit net amounts; tax and supplier bills excluded.|已开本币发票未税金额减已开客户贷项未税金额；不含税及供应商账单。|已開本幣發票未稅金額減已開客戶貸項未稅金額；不含稅及供應商帳單。|Factures émises nettes en devise locale moins les crédits clients émis; taxes et factures fournisseurs exclues.
Filters · category, customer, group, salesperson & margin|筛选 · 类别、客户、组、销售员与毛利|篩選 · 類別、客戶、群組、業務員與毛利|Filtres · catégorie, client, groupe, vendeur et marge
Sign in to Harbor|登录 Harbor|登入 Harbor|Se connecter à Harbor
Use a keyboard scanner, type a SKU, or choose Camera. Each scan must be saved once.|使用键盘扫码器、输入 SKU 或选择相机。每次扫码仅保存一次。|使用鍵盤掃碼器、輸入 SKU 或選擇相機。每次掃碼僅儲存一次。|Utilisez un lecteur clavier, saisissez un SKU ou choisissez Caméra. Chaque lecture doit être enregistrée une seule fois.
Review and issue|审核并开立|審核並開立|Vérifier et émettre
Open record|打开记录|開啟記錄|Ouvrir
Document / source|单据 / 来源|單據 / 來源|Document / source
Date / due|日期 / 到期日|日期 / 到期日|Date / échéance
No due date|无到期日|無到期日|Sans date d’échéance
Drafts do not affect balances.|草稿不影响余额。|草稿不影響餘額。|Les brouillons n’affectent pas les soldes.
Local billing records share your saved warehouse data. Payment entries record money received or sent elsewhere.|本地账务记录使用已保存的仓库数据。付款记录登记在其他地方收付的款项。|本機帳務記錄使用已儲存的倉庫資料。付款記錄登記在其他地方收付的款項。|La facturation locale utilise les données enregistrées de l’entrepôt. Les paiements consignent les fonds reçus ou envoyés ailleurs.
Line total|行总额|列總額|Total de ligne
Net|未税金额|未稅金額|Net
Credits|贷项|貸項|Crédits
Paid / refunded|已付 / 已退|已付 / 已退|Payé / remboursé
Balance due|应付余额|應付餘額|Solde dû
Record / document|记录 / 单据|記錄 / 單據|Enregistrement / document
Direction / date|方向 / 日期|方向 / 日期|Sens / date
Amount|金额|金額|Montant
Linked credit|关联贷项|關聯貸項|Crédit lié
Document history|单据历史|單據歷史|Historique du document
All purchases|所有采购|所有採購|Tous les achats
Approval & revision history|审批与修订历史|審批與修訂歷史|Historique des approbations et révisions
Confirmed arrival|已确认到货日|已確認到貨日|Arrivée confirmée
Active|启用|啟用|Actif
Archived|已归档|已封存|Archivé
Supplier product codes|供应商产品代码|供應商產品代碼|Codes produits des fournisseurs
Optional: use your supplier’s code alongside your warehouse SKU.|可选：在仓库 SKU 旁使用供应商货号。|選填：在倉庫 SKU 旁使用供應商貨號。|Facultatif : utilisez le code fournisseur avec votre SKU d’entrepôt.
Chinese and English supplier details, contacts and product codes.|中英文供应商资料、联系人及产品代码。|中英文供應商資料、聯絡人及產品代碼。|Coordonnées, contacts et codes produits des fournisseurs en chinois et en anglais.
English name|英文名称|英文名稱|Nom anglais
Email / phone|电子邮箱 / 电话|電子郵件 / 電話|Courriel / téléphone
Supplier total|供应商总额|供應商總額|Total fournisseur
Ordered|已订购|已訂購|Commandé
Receiving history|收货历史|收貨歷史|Historique des réceptions
Revision|修订版本|修訂版本|Révision
Operator|操作人|操作人|Opérateur
Action / reason|操作 / 原因|操作 / 原因|Action / motif
Not confirmed|尚未确认|尚未確認|Non confirmé
Draft created|已创建草稿|已建立草稿|Brouillon créé
Submitted for approval|已提交审批|已提交審批|Soumis pour approbation
Amounts use the workspace currency. Supplier and product text on new purchase orders is retained as issued.|金额使用工作区币种。新采购订单的供应商和产品文字按下单时保留。|金額使用工作區幣別。新採購訂單的供應商及產品文字依下單時保留。|Les montants utilisent la devise de l’espace de travail. Les textes fournisseurs et produits sont conservés tels qu’émis.
Main navigation|主导航|主導覽|Navigation principale
Interface view|界面视图|介面檢視|Vue de l’interface
Bill multiple receipts / 合并收货 / 合併收貨|合并收货账单|合併收貨帳單|Facturer plusieurs réceptions
Document language / 中文单据|单据语言|單據語言|Langue du document
Description / 描述 / 說明|产品说明|產品說明|Description
I reviewed the document before issuing it.|我已审核单据后再开立。|我已審核單據後再開立。|J’ai vérifié le document avant son émission.
Account access|账户权限|帳戶權限|Accès au compte
Accounts|账户|帳戶|Comptes
Actual quantity counted|实际盘点数量|實際盤點數量|Quantité réellement comptée
Add Carton|添加箱子|新增箱子|Ajouter un colis
Add Stock|添加库存|新增庫存|Ajouter du stock
Add account|添加账户|新增帳戶|Ajouter un compte
Add landed cost|添加到岸成本|新增到岸成本|Ajouter un coût d’approche
Add product|添加产品|新增產品|Ajouter un produit
Add product code|添加产品代码|新增產品代碼|Ajouter un code produit
Address line 1|地址第一行|地址第一行|Adresse ligne 1
Address line 2|地址第二行|地址第二行|Adresse ligne 2
Affected units|受影响数量|受影響數量|Unités concernées
Allocate by|分摊依据|分攤依據|Base de répartition
Allocate cost|分摊成本|分攤成本|Répartir le coût
Allocate landed costs|分摊到岸成本|分攤到岸成本|Répartir les coûts d’approche
Allocated|已分配|已分配|Affecté
Apply supplier prices|应用供应商价格|套用供應商價格|Appliquer les prix fournisseurs
Approval policy|审批规则|審批規則|Politique d’approbation
Approval reason|批准原因|批准原因|Motif d’approbation
Approve|批准|批准|Approuver
Approve & post|批准并过账|批准並過帳|Approuver et comptabiliser
Approve and post count|批准并过账盘点|批准並過帳盤點|Approuver et comptabiliser l’inventaire
Approve purchase|批准采购|批准採購|Approuver l’achat
As of date|截至日期|截至日期|Date de référence
Average Cost|平均成本|平均成本|Coût moyen
Average unit cost|平均单位成本|平均單位成本|Coût unitaire moyen
Back up now|立即备份|立即備份|Sauvegarder maintenant
Backups & browser archives|备份与浏览器存档|備份與瀏覽器封存|Sauvegardes et archives du navigateur
Barcode (optional; SKU also scans)|条码（可选；也可扫描 SKU）|條碼（選填；也可掃描 SKU）|Code-barres (facultatif; le SKU fonctionne aussi)
Barcode label|条码标签|條碼標籤|Étiquette code-barres
Bill multiple receipts|合并收货账单|合併收貨帳單|Facturer plusieurs réceptions
Bill of materials|物料清单|物料清單|Nomenclature
Business details|公司信息|公司資訊|Coordonnées de l’entreprise
Business details for billing|开票公司信息|開票公司資訊|Coordonnées de facturation de l’entreprise
Business name|公司名称|公司名稱|Nom de l’entreprise
Cancel balance|取消余量|取消餘量|Annuler le reliquat
Cancel draft|取消草稿|取消草稿|Annuler le brouillon
Cancel order|取消订单|取消訂單|Annuler la commande
Cancel remaining balance?|取消剩余数量？|取消剩餘數量？|Annuler le reliquat ?
Cancel session|取消盘点任务|取消盤點工作|Annuler la session
Cancel unsent preview|取消未发送预览|取消未傳送預覽|Annuler l’aperçu non envoyé
Cancellation reason|取消原因|取消原因|Motif d’annulation
Carrier|承运商|承運商|Transporteur
Carrier (optional)|承运商（可选）|承運商（選填）|Transporteur (facultatif)
Carrier Service|承运服务|承運服務|Service du transporteur
Carton name|箱子名称|箱子名稱|Nom du colis
Carton tracking reference|箱子追踪编号|箱子追蹤編號|Référence de suivi du colis
Cartons|箱子|箱子|Colis
Change website|更改网站|變更網站|Changer le site web
Charge type|费用类型|費用類型|Type de frais
Chart view|图表视图|圖表檢視|Vue graphique
Check sandbox result|检查沙盒结果|檢查沙盒結果|Vérifier le résultat du bac à sable
Checkpoint label / 名称 / 名稱|检查点名称|檢查點名稱|Nom du point de contrôle
Choose PO for a combined supplier bill|选择要合并开票的采购订单|選擇要合併開票的採購訂單|Choisir les commandes pour une facture groupée
Choose QuickBooks mapping|选择 QuickBooks 映射|選擇 QuickBooks 對應|Choisir la correspondance QuickBooks
Choose a document|选择单据|選擇單據|Choisir un document
Choose mapping|选择映射|選擇對應|Choisir une correspondance
Choose report & filters|选择报表与筛选|選擇報表與篩選|Choisir le rapport et les filtres
Clear filters|清除筛选|清除篩選|Effacer les filtres
Close Tab|关闭页签|關閉頁籤|Fermer l’onglet
Close sales order short|短缺结清销售订单|短缺結清銷售訂單|Clôturer la commande avec un reliquat non livré
Close short|短缺结清|短缺結清|Clôturer avec reliquat
Code|代码|代碼|Code
Columns|列|欄|Colonnes
Combine|合并|合併|Regrouper
Combine picks|合并拣货|合併揀貨|Regrouper les préparations
Commit Batch|分配整批|分配整批|Affecter le lot
Compare inventory value|比较库存价值|比較庫存價值|Comparer la valeur des stocks
Compare sandbox balances|比较沙盒余额|比較沙盒餘額|Comparer les soldes du bac à sable
Complete build|完成生产|完成生產|Terminer la fabrication
Confirm|确认|確認|Confirmer
Contact person|联系人|聯絡人|Personne-ressource
Count method|盘点方式|盤點方式|Méthode de comptage
Count sheet / PDF|盘点表 / PDF|盤點表 / PDF|Feuille de comptage / PDF
Counted quantity|已盘数量|已盤數量|Quantité comptée
Create a supplier first|请先创建供应商|請先建立供應商|Créer d’abord un fournisseur
Create credit note|创建贷项通知单|建立貸項通知單|Créer une note de crédit
Create forecast purchase draft|创建预测采购草稿|建立預測採購草稿|Créer un brouillon d’achat prévisionnel
Create in sandbox|在沙盒中创建|在沙盒中建立|Créer dans le bac à sable
Create proposals|创建建议|建立建議|Créer des propositions
Create purchase draft|创建采购草稿|建立採購草稿|Créer un brouillon d’achat
Create user account|创建用户账户|建立使用者帳戶|Créer un compte utilisateur
Created|创建时间|建立時間|Créé
Credit date|贷项日期|貸項日期|Date du crédit
Currency purchase order|外币采购订单|外幣採購訂單|Commande fournisseur en devise
Current stock|当前库存|目前庫存|Stock actuel
Customer (direct deliveries)|客户（直送）|客戶（直送）|Client (livraisons directes)
Customer code|客户代码|客戶代碼|Code client
Customer group|客户组|客戶群組|Groupe de clients
Customer groups|客户组|客戶群組|Groupes de clients
Customer name|客户名称|客戶名稱|Nom du client
Customer reference|客户参考编号|客戶參考編號|Référence client
Damaged units|破损数量|破損數量|Unités endommagées
Dashboard settings|仪表板设置|儀表板設定|Paramètres du tableau de bord
Dashboard website link|仪表板网站链接|儀表板網站連結|Lien web du tableau de bord
Date Range|日期范围|日期範圍|Période
Date Shipped|发货日期|出貨日期|Date d’expédition
Delivery note (optional)|送货备注（可选）|送貨備註（選填）|Note de livraison (facultatif)
Delivery note / reference|送货备注 / 参考编号|送貨備註 / 參考編號|Note / référence de livraison
Delivery type|交货类型|交貨類型|Type de livraison
Development Client ID|开发 Client ID|開發 Client ID|ID client de développement
Development Client Secret|开发 Client Secret|開發 Client Secret|Secret client de développement
Dimension unit|尺寸单位|尺寸單位|Unité de dimension
Disconnect sandbox|断开沙盒连接|中斷沙盒連線|Déconnecter le bac à sable
Discount %|折扣 %|折扣 %|Remise %
Dispatch|发运|發運|Expédier
Dispatch in full on time|按时足量发运|準時足量發運|Expédition complète à temps
Display name|显示名称|顯示名稱|Nom affiché
Download|下载|下載|Télécharger
Download label SVG|下载 SVG 标签|下載 SVG 標籤|Télécharger l’étiquette SVG
Download report CSV|下载报表 CSV|下載報表 CSV|Télécharger le rapport CSV
Download reviewed journals|下载已审核凭证|下載已審核憑證|Télécharger les écritures vérifiées
Download round CSV|下载盘点轮次 CSV|下載盤點輪次 CSV|Télécharger le tour de comptage CSV
Download shipment notices|下载发货通知|下載出貨通知|Télécharger les avis d’expédition
Download sync history|下载同步历史|下載同步歷史|Télécharger l’historique de synchronisation
Drop Ship|直送|直送|Livraison directe
Edit Details|编辑详情|編輯詳細資料|Modifier les détails
Edit Fields|编辑字段|編輯欄位|Modifier les champs
Edit Text|编辑文字|編輯文字|Modifier le texte
Edit draft|编辑草稿|編輯草稿|Modifier le brouillon
Edit rules|编辑规则|編輯規則|Modifier les règles
Edit supplier|编辑供应商|編輯供應商|Modifier le fournisseur
Edit text|编辑文字|編輯文字|Modifier le texte
Edit tracking|编辑追踪信息|編輯追蹤資訊|Modifier le suivi
Enable / disable account|启用 / 停用账户|啟用 / 停用帳戶|Activer / désactiver le compte
Enable receipt accounting|启用收货会计|啟用收貨會計|Activer la comptabilisation des réceptions
End date (optional)|结束日期（可选）|結束日期（選填）|Date de fin (facultatif)
Enter development keys|输入开发密钥|輸入開發金鑰|Saisir les clés de développement
Exact lot or serial|准确批次或序列号|確切批次或序號|Lot ou numéro de série exact
Expiration date (optional)|到期日（可选）|到期日（選填）|Date d’expiration (facultatif)
Export backup|导出备份|匯出備份|Exporter une sauvegarde
Export billing CSV|导出账务 CSV|匯出帳務 CSV|Exporter la facturation CSV
Export count CSV|导出盘点 CSV|匯出盤點 CSV|Exporter le comptage CSV
Export matching CSV|导出匹配 CSV|匯出比對 CSV|Exporter le rapprochement CSV
Export payment CSV|导出付款 CSV|匯出付款 CSV|Exporter les paiements CSV
Export trace JSON|导出追溯 JSON|匯出追溯 JSON|Exporter la traçabilité JSON
Filter billing documents|筛选账务单据|篩選帳務單據|Filtrer les documents de facturation
Finish Batch|完成整批|完成整批|Terminer le lot
Finish pick|完成拣货|完成揀貨|Terminer la préparation
Finished goods destination|成品入库库位|成品入庫庫位|Destination des produits finis
Finished product|成品|成品|Produit fini
Forecast assumptions|预测假设|預測假設|Hypothèses de prévision
Freight / expense reference|运费 / 费用参考编号|運費 / 費用參考編號|Référence de transport / dépense
From date (optional)|开始日期（可选）|開始日期（選填）|Date de début (facultatif)
Fulfillment|履行|履行|Exécution
Group|组|群組|Groupe
HTTPS website address|HTTPS 网站地址|HTTPS 網站位址|Adresse du site HTTPS
High-value review threshold (|高金额审核阈值（|高金額審核門檻（|Seuil de vérification des achats élevés (
Hold reason|冻结原因|凍結原因|Motif de blocage
Home currency per currency unit|每外币单位的本币金额|每外幣單位的本幣金額|Devise locale par unité de devise
Import partner order|导入伙伴订单|匯入夥伴訂單|Importer une commande partenaire
Inactive customers|停用客户|停用客戶|Clients inactifs
Inspect / put away|检验 / 上架|檢驗 / 上架|Inspecter / ranger
Inspect damaged goods|检验破损货物|檢驗破損貨物|Inspecter les marchandises endommagées
Inspection reason|检验原因|檢驗原因|Motif d’inspection
Instructions|说明|說明|Instructions
Inventory owner|库存货主|庫存貨主|Propriétaire des stocks
Invoice / bill|发票 / 账单|發票 / 帳單|Facture client / fournisseur
Issue locally|本地下单|本機下單|Émettre localement
Issue order|下达订单|下達訂單|Émettre la commande
Kit|套件|套件|Kit
Label|标签|標籤|Étiquette
Linked fulfillment / backorders|关联履行 / 欠交订单|關聯履行 / 欠交訂單|Exécution liée / reliquats
Load Layout|载入布局|載入版面|Charger la disposition
Load sandbox lists|载入沙盒列表|載入沙盒清單|Charger les listes du bac à sable
Lookback days (30–365; weighted uses 90)|回溯天数（30–365；加权使用 90）|回溯天數（30–365；加權使用 90）|Jours d’historique (30–365; pondéré : 90)
Lot (optional)|批次（可选）|批次（選填）|Lot (facultatif)
Lot expiration date|批次到期日|批次到期日|Date d’expiration du lot
Margin level|毛利水平|毛利水準|Niveau de marge
Mark reviewed|标记已审核|標記已審核|Marquer comme vérifié
Maximum purchase amount (|采购金额上限（|採購金額上限（|Montant maximal d’achat (
Move stock|移动库存|移動庫存|Déplacer le stock
Net amount (zero tax)|未税金额（零税）|未稅金額（零稅）|Montant net (taxe nulle)
New Order|新建订单|新增訂單|Nouvelle commande
New Part|新建产品|新增產品|Nouveau produit
New Tab|新建页签|新增頁籤|Nouvel onglet
New bill of materials|新建物料清单|新增物料清單|Nouvelle nomenclature
New count session|新建盘点任务|新增盤點工作|Nouvelle session de comptage
New credit note|新建贷项|新增貸項|Nouvelle note de crédit
New customer|新建客户|新增客戶|Nouveau client
New cycle count|新建循环盘点|新增循環盤點|Nouvel inventaire tournant
New inventory owner|新建库存货主|新增庫存貨主|Nouveau propriétaire de stocks
New kit|新建套件|新增套件|Nouveau kit
New landed charge bill|新建到岸费用账单|新增到岸費用帳單|Nouvelle facture de frais d’approche
New scoped location|新建指定范围库位|新增指定範圍庫位|Nouvel emplacement dans le périmètre
New transfer|新建调拨|新增調撥|Nouveau transfert
New warehouse|新建仓库|新增倉庫|Nouvel entrepôt
New work order|新建工单|新增工單|Nouvel ordre de fabrication
Not Available|不可用|無法使用|Non disponible
Open count|打开盘点|開啟盤點|Ouvrir le comptage
Open credit|打开贷项|開啟貸項|Ouvrir le crédit
Open document|打开单据|開啟單據|Ouvrir le document
Open estimates — draft sales orders|未完成报价 — 草稿销售订单|未完成報價 — 草稿銷售訂單|Devis ouverts — commandes clients brouillons
Open original document|打开原始单据|開啟原始單據|Ouvrir le document d’origine
Opening snapshot label / 名称 / 名稱|期初快照名称|期初快照名稱|Nom de l’instantané initial
Order Items|订单产品|訂單產品|Articles de la commande
Order Number|订单编号|訂單編號|Numéro de commande
Order details|订单详情|訂單詳細資料|Détails de la commande
Order reference|订单参考编号|訂單參考編號|Référence de commande
Original order|原始订单|原始訂單|Commande d’origine
Owner / customer name|货主 / 客户名称|貨主 / 客戶名稱|Nom du propriétaire / client
PO / supplier|采购单 / 供应商|採購單 / 供應商|Commande / fournisseur
Pack shipment|包装发货|包裝出貨|Emballer l’expédition
Packing|包装|包裝|Emballage
Packing / Tracking|包装 / 追踪|包裝 / 追蹤|Emballage / suivi
Packing Slip|装箱单|裝箱單|Bordereau de livraison
Part Description|产品说明|產品說明|Description du produit
Part Number|产品编号|產品編號|Numéro de produit
Password (10+ characters)|密码（至少 10 个字符）|密碼（至少 10 個字元）|Mot de passe (10 caractères ou plus)
Payment date|付款日期|付款日期|Date de paiement
Pick Location|拣货库位|揀貨庫位|Emplacement de préparation
Pick Number|拣货单号|揀貨單號|Numéro de préparation
Pick details|拣货详情|揀貨詳細資料|Détails de préparation
Preferred Supplier|首选供应商|首選供應商|Fournisseur préféré
Prepare new sandbox record|准备新的沙盒记录|準備新的沙盒記錄|Préparer un nouvel enregistrement de test
Prepare preview|准备预览|準備預覽|Préparer l’aperçu
Previous Date Range|上一日期范围|上一日期範圍|Période précédente
Price per stock unit|每库存单位价格|每庫存單位價格|Prix par unité de stock
Priced sales order|已定价销售订单|已定價銷售訂單|Commande client tarifée
Pricing rule|定价规则|定價規則|Règle de tarification
Print Labels|打印标签|列印標籤|Imprimer les étiquettes
Print dashboard|打印仪表板|列印儀表板|Imprimer le tableau de bord
Print labels|打印标签|列印標籤|Imprimer les étiquettes
Printable warehouse labels|可打印仓库标签|可列印倉庫標籤|Étiquettes d’entrepôt imprimables
Priority|优先级|優先順序|Priorité
Product barcode label|产品条码标签|產品條碼標籤|Étiquette code-barres du produit
Product category|产品类别|產品類別|Catégorie de produit
Products not sold|未售产品|未售產品|Produits non vendus
Promised dispatch date|承诺发运日期|承諾發運日期|Date d’expédition promise
Promised dispatch date & salesperson|承诺发运日期与销售员|承諾發運日期與業務員|Date d’expédition promise et vendeur
Purchase|采购|採購|Achat
Purchase approval policy|采购审批规则|採購審批規則|Politique d’approbation des achats
Purchase order / 采购单|采购订单|採購訂單|Commande fournisseur
Purchase unit name|采购单位名称|採購單位名稱|Nom de l’unité d’achat
Purchases|采购记录|採購記錄|Achats
Purchases for this product|此产品的采购记录|此產品的採購記錄|Achats pour ce produit
Quantity to close|结清数量|結清數量|Quantité à clôturer
Quantity to move|移动数量|移動數量|Quantité à déplacer
Quantity to scrap|报废数量|報廢數量|Quantité à mettre au rebut
QuickBooks record|QuickBooks 记录|QuickBooks 記錄|Enregistrement QuickBooks
QuickBooks sandbox development keys|QuickBooks 沙盒开发密钥|QuickBooks 沙盒開發金鑰|Clés de développement du bac à sable QuickBooks
Reason (optional)|原因（可选）|原因（選填）|Motif (facultatif)
Recall preview / PDF|召回预览 / PDF|召回預覽 / PDF|Aperçu du rappel / PDF
Receipt ID (required for controlled PO)|收货 ID（受控采购必填）|收貨 ID（受控採購必填）|ID de réception (requis pour les achats contrôlés)
Receiving location|收货库位|收貨庫位|Emplacement de réception
Recipient|收件人|收件人|Destinataire
Record a preserved inventory checkpoint|记录保存的库存检查点|記錄保存的庫存檢查點|Enregistrer un point de contrôle conservé
Record comparison baseline|记录对账基准|記錄對帳基準|Enregistrer la base de comparaison
Record cycle count|记录循环盘点|記錄循環盤點|Enregistrer un inventaire tournant
Record discrepancy|记录差异|記錄差異|Enregistrer un écart
Record inventory comparison baseline|记录库存对账基准|記錄庫存對帳基準|Enregistrer la base de comparaison des stocks
Record payment / refund|记录付款 / 退款|記錄付款 / 退款|Enregistrer un paiement / remboursement
Record receipt discrepancy|记录收货差异|記錄收貨差異|Enregistrer un écart de réception
Recorded closed-short items|已记录短缺结清产品|已記錄短缺結清產品|Articles clôturés avec reliquat
Recount reason|复盘原因|複盤原因|Motif du recomptage
Refresh view|刷新视图|重新整理檢視|Actualiser la vue
Reject|拒绝|拒絕|Refuser
Release Batch|释放整批|釋放整批|Libérer le lot
Remove product|移除产品|移除產品|Retirer le produit
Remove product code|移除产品代码|移除產品代碼|Retirer le code produit
Rename Tab|重命名页签|重新命名頁籤|Renommer l’onglet
Replace shared records with this browser copy?|用此浏览器副本替换共享记录？|以此瀏覽器副本取代共用記錄？|Remplacer les enregistrements partagés par cette copie ?
Report|报表|報表|Rapport
Report and filters|报表与筛选|報表與篩選|Rapport et filtres
Require a different administrator|要求另一位管理员|要求另一位管理員|Exiger un autre administrateur
Reserve stock|预留库存|預留庫存|Réserver les stocks
Reset the workspace?|重置工作区？|重設工作區？|Réinitialiser l’espace de travail ?
Restore this backup?|恢复此备份？|還原此備份？|Restaurer cette sauvegarde ?
Return from original receipt|从原始收货退货|從原始收貨退貨|Retourner depuis la réception d’origine
Return from receipt|从收货退货|從收貨退貨|Retourner depuis une réception
Return quantity|退货数量|退貨數量|Quantité retournée
Return to draft|退回草稿|退回草稿|Revenir au brouillon
Reverse entry|冲销记录|沖銷記錄|Contrepasser l’écriture
Reverse packing|撤销包装|撤銷包裝|Annuler l’emballage
Reverse pick|撤销拣货|撤銷揀貨|Annuler la préparation
Reverse shipment|撤销发货|撤銷出貨|Annuler l’expédition
Reverse shipment / packing|撤销发货 / 包装|撤銷出貨 / 包裝|Annuler l’expédition / emballage
Review|审核|審核|Vérifier
Review & issue|审核并开立|審核並開立|Vérifier et émettre
Review PO / receipt / bill|审核采购单 / 收货 / 账单|審核採購單 / 收貨 / 帳單|Vérifier commande / réception / facture
Review browser replacement|审核浏览器替换|審核瀏覽器取代|Vérifier le remplacement par le navigateur
Review catalog import|审核目录导入|審核目錄匯入|Vérifier l’importation du catalogue
Review currency payable account|审核外币应付账户|審核外幣應付帳戶|Vérifier le compte fournisseur en devise
Review document exchange rate|审核单据汇率|審核單據匯率|Vérifier le taux de change du document
Review interval days|审核周期天数|審核週期天數|Intervalle de vérification en jours
Review match|审核匹配|審核比對|Vérifier le rapprochement
Review reason|审核原因|審核原因|Motif de vérification
Review saved bill payable account|审核已存账单应付账户|審核已存帳單應付帳戶|Vérifier le compte fournisseur de la facture enregistrée
Review sync|审核同步|審核同步|Vérifier la synchronisation
Reviewed price per stock unit (|已审核每库存单位价格（|已審核每庫存單位價格（|Prix vérifié par unité de stock (
Revise|修订|修訂|Réviser
Role|角色|角色|Rôle
Safety days|安全库存天数|安全庫存天數|Jours de sécurité
Sales Order|销售订单|銷售訂單|Commande client
Sales details|销售详情|銷售詳細資料|Détails des ventes
Sales goal|销售目标|銷售目標|Objectif de ventes
Sales pricing|销售定价|銷售定價|Tarification des ventes
Salesperson|销售员|業務員|Vendeur
Sandbox Company ID|沙盒公司 ID|沙盒公司 ID|ID de société du bac à sable
Save Layout|保存布局|儲存版面|Enregistrer la disposition
Scan barcode or SKU|扫描条码或 SKU|掃描條碼或 SKU|Lire un code-barres ou SKU
Scan count|扫码盘点|掃碼盤點|Comptage par lecture
Scan pick|扫码拣货|掃碼揀貨|Préparation par lecture
Scan receipt|扫码收货|掃碼收貨|Réception par lecture
Scheduled|已排期|已排程|Planifié
Scheduled date|排期日期|排程日期|Date planifiée
Search details|搜索详情|搜尋詳細資料|Détails de recherche
Search lot / serial|搜索批次 / 序列号|搜尋批次 / 序號|Rechercher un lot / numéro de série
Search number, party or reference|搜索编号、对方或参考编号|搜尋編號、對方或參考編號|Rechercher un numéro, tiers ou référence
Sell a kit|销售套件|銷售套件|Vendre un kit
Send to supplier|发送给供应商|傳送給供應商|Envoyer au fournisseur
Serial numbers (comma separated if required)|序列号（如需要，以逗号分隔）|序號（如需要，以逗號分隔）|Numéros de série (séparés par des virgules si requis)
Server audit|服务器审计|伺服器稽核|Audit du serveur
Server audit — latest 500 writes|服务器审计 — 最近 500 次写入|伺服器稽核 — 最近 500 次寫入|Audit du serveur — 500 dernières écritures
Service (record only)|服务（仅记录）|服務（僅記錄）|Service (enregistrement seulement)
Session name|任务名称|工作名稱|Nom de session
Set Cost|设置成本|設定成本|Définir le coût
Set goal|设置目标|設定目標|Définir l’objectif
Settings|设置|設定|Paramètres
Shared backups|共享备份|共用備份|Sauvegardes partagées
Ship Items|发货产品|出貨產品|Articles à expédier
Ship To|收货人|收貨人|Destinataire
Ship order|发运订单|發運訂單|Expédier la commande
Shipment|发货单|出貨單|Expédition
Shipment details|发货详情|出貨詳細資料|Détails de l’expédition
Shipping Cost|运费|運費|Frais d’expédition
Slot|位置|位置|Position
Slot / cart position|位置 / 拣货车位置|位置 / 揀貨車位置|Position / emplacement du chariot
Sort by revenue|按收入排序|依收入排序|Trier par chiffre d’affaires
Source stock|来源库存|來源庫存|Stock source
Split|拆分|拆分|Fractionner
Split fulfillment / backorder|拆分履行 / 欠交订单|拆分履行 / 欠交訂單|Fractionner l’exécution / reliquat
Start|开始|開始|Commencer
Start date (optional)|开始日期（可选）|開始日期（選填）|Date de début (facultatif)
Start historical inventory recording|开始记录历史库存|開始記錄歷史庫存|Commencer l’historique des stocks
Start production|开始生产|開始生產|Démarrer la fabrication
Start recount|开始复盘|開始複盤|Commencer le recomptage
Submit for approval|提交审批|提交審批|Soumettre pour approbation
Submit for review|提交审核|提交審核|Soumettre pour vérification
Supplier code|供应商代码|供應商代碼|Code fournisseur
Supplier confirmation reference|供应商确认编号|供應商確認編號|Référence de confirmation du fournisseur
Supplier invoice number|供应商发票号|供應商發票號|Numéro de facture fournisseur
Supplier invoice reference|供应商发票参考编号|供應商發票參考編號|Référence de facture fournisseur
Supplier name (local / Chinese)|供应商名称（本地 / 中文）|供應商名稱（當地 / 中文）|Nom du fournisseur (local / chinois)
Supplier price|供应商价格|供應商價格|Prix fournisseur
Supplier reference|供应商参考编号|供應商參考編號|Référence fournisseur
Supplier-confirmed arrival date|供应商确认到货日期|供應商確認到貨日期|Date d’arrivée confirmée par le fournisseur
Tab name|页签名称|頁籤名稱|Nom de l’onglet
Tax %|税率 %|稅率 %|Taxe %
Tax label|税额标签|稅額標籤|Libellé de taxe
Tax registration (optional)|税务登记号（可选）|稅務登記號（選填）|Inscription fiscale (facultatif)
This year’s sales goal (|本年度销售目标（|本年度銷售目標（|Objectif de ventes de l’année (
Through date (optional)|截至日期（可选）|截至日期（選填）|Jusqu’au (facultatif)
Total Cost|总成本|總成本|Coût total
Total Inventory Value|库存总价值|庫存總價值|Valeur totale des stocks
Trace a lot or serial|追溯批次或序列号|追溯批次或序號|Tracer un lot ou numéro de série
Tracking Number|追踪编号|追蹤編號|Numéro de suivi
Tracking mode|追踪模式|追蹤模式|Mode de suivi
Tracking reference|追踪参考编号|追蹤參考編號|Référence de suivi
Tracking reference (optional)|追踪参考编号（可选）|追蹤參考編號（選填）|Référence de suivi (facultatif)
Transaction reference|交易参考编号|交易參考編號|Référence de transaction
Transfer note|调拨备注|調撥備註|Note de transfert
Try again|重试|重試|Réessayer
Unit cost (optional)|单位成本（可选）|單位成本（選填）|Coût unitaire (facultatif)
User|用户|使用者|Utilisateur
User accounts|用户账户|使用者帳戶|Comptes utilisateurs
View stock|查看库存|檢視庫存|Voir le stock
Void|作废|作廢|Annuler
Warehouse replenishment rule|仓库补货规则|倉庫補貨規則|Règle de réapprovisionnement de l’entrepôt
Warehouse rules|仓库规则|倉庫規則|Règles de l’entrepôt
Warehouse tools|仓库工具|倉庫工具|Outils d’entrepôt
Weight unit|重量单位|重量單位|Unité de poids
Your first order, step by step|您的首笔订单操作步骤|您的首筆訂單操作步驟|Votre première commande, étape par étape
Costs are saved locally and included in backups.|成本保存在本地，并包含在备份中。|成本儲存於本機，並包含於備份中。|Les coûts sont conservés localement et inclus dans les sauvegardes.
FIFO inventory value is the sum of remaining receipt layers; the next-unit cost follows the oldest active layer. Historical valuation is available under Accounting.|FIFO 库存价值为剩余收货成本层合计；下一件成本来自最早的有效成本层。历史估值位于会计菜单。|FIFO 庫存價值為剩餘收貨成本層合計；下一件成本來自最早的有效成本層。歷史估值位於會計選單。|La valeur FIFO est la somme des couches de réception restantes; le prochain coût suit la plus ancienne couche active. L’évaluation historique se trouve sous Comptabilité.
Customer returns create new dated layers at the audited original-shipment cost plus supported later costs. Inspection scrap uses the return’s own cost slices. Late bill/freight adjustments preserve old journals. FIFO production, supplier-return settlement, cross-warehouse transfers and uncosted count increases require separate workflows.|客户退货按审核后的原发货成本及支持的后续成本建立新日期成本层。检验报废使用该退货的成本明细。后续账单 / 运费调整保留旧凭证。FIFO 生产、供应商退货结算、跨仓调拨及无成本盘盈需专门流程。|客戶退貨依審核後的原出貨成本及支援的後續成本建立新日期成本層。檢驗報廢使用該退貨的成本明細。後續帳單 / 運費調整保留舊憑證。FIFO 生產、供應商退貨結算、跨倉調撥及無成本盤盈需專門流程。|Les retours créent de nouvelles couches datées au coût d’expédition d’origine vérifié, plus les coûts ultérieurs pris en charge. Le rebut utilise les coûts du retour. Les ajustements préservent les anciennes écritures. La production FIFO, les retours fournisseurs, les transferts interentrepôts et les hausses sans coût exigent des flux dédiés.
Dispatch book value|发出账面价值|發出帳面價值|Valeur comptable expédiée
Current transit value|当前在途价值|目前在途價值|Valeur actuelle en transit
Cost / PDF|成本 / PDF|成本 / PDF|Coût / PDF
FIFO warehouse transfer|FIFO 仓库调拨|FIFO 倉庫調撥|Transfert FIFO entre entrepôts
FIFO supplier return|FIFO 供应商退货|FIFO 供應商退貨|Retour fournisseur FIFO
FIFO cost document|FIFO 成本文档|FIFO 成本文件|Document de coûts FIFO
Origin warehouse|发出仓库|發出倉庫|Entrepôt d'origine
Destination warehouse|接收仓库|接收倉庫|Entrepôt de destination
Warehouse / transit|仓库 / 在途|倉庫 / 在途|Entrepôt / transit
Original layer date|原成本层日期|原成本層日期|Date de la couche d'origine
Unit range|单位范围|單位範圍|Plage des unités
Supplier credit amount|供应商贷项金额|供應商貸項金額|Montant du crédit fournisseur
Settlement adjustment|结算调整|結算調整|Ajustement de règlement
Dispatched|已发出|已發出|Expédié
Ordinary transfer preserves company inventory value. Later receipt costs are separate adjustments.|普通调拨保留公司库存价值。后续收货成本作为单独调整。|一般調撥保留公司庫存價值。後續收貨成本列為獨立調整。|Le transfert ordinaire préserve la valeur du stock de la société. Les coûts ultérieurs de réception font l'objet d'ajustements distincts.
FIFO dispatch value is frozen. The selected receipt identifies the supplier credit; oldest available warehouse layers determine book cost.|FIFO 发出价值已冻结。所选收货记录用于供应商贷项；仓库中最早可用成本层决定账面成本。|FIFO 發出價值已凍結。所選收貨記錄用於供應商貸項；倉庫內最早可用成本層決定帳面成本。|La valeur FIFO expédiée est figée. La réception choisie identifie le crédit fournisseur; les plus anciennes couches disponibles de l'entrepôt déterminent le coût comptable.
Supplier returns consume oldest available warehouse FIFO ranges. Transfers retain origin dates and costs through transit and partial receipt. Late costs preserve old postings. Production and uncosted increases remain blocked.|供应商退货消耗仓库中最早可用 FIFO 范围。调拨在在途及分批接收时保留原日期和成本。后续成本保留旧凭证。生产及无成本盘盈仍受限。|供應商退貨消耗倉庫內最早可用 FIFO 範圍。調撥在在途及分批接收時保留原日期與成本。後續成本保留舊憑證。生產及無成本盤盈仍受限。|Les retours fournisseurs consomment les plus anciennes plages FIFO disponibles. Les transferts conservent les dates et coûts en transit et lors des réceptions partielles. Les coûts ultérieurs préservent les écritures. La production et les hausses sans coût restent bloquées.
Prospective FIFO starts in one owned warehouse and supports transfer orders. Existing products and average costs cannot be converted. Production and uncosted increases remain blocked.|前瞻 FIFO 从一个自有仓库开始，支持调拨单。不转换现有产品及平均成本。生产及无成本盘盈仍受限。|前瞻 FIFO 從一個自有倉庫開始，支援調撥單。不轉換現有產品及平均成本。生產及無成本盤盈仍受限。|FIFO démarre dans un entrepôt détenu et prend en charge les transferts. Les produits existants et leurs coûts moyens ne sont pas convertis. La production et les hausses sans coût restent bloquées.
Transfer|调拨|調撥|Transfert
Product / origin|产品 / 发出地|產品 / 發出地|Produit / origine
Received / quantity|已收货 / 数量|已收貨 / 數量|Reçu / quantité
In transit|在途|在途|En transit
Transfer dispatched|调拨已发出|調撥已發出|Transfert expédié
Transfer received|调拨已接收|調撥已接收|Transfert reçu
Draft → dispatch → in transit → receive. Partial receipts retain the remaining stock in transit.|草稿 → 发出 → 在途 → 收货。分批收货保留剩余在途库存。|草稿 → 發出 → 在途 → 收貨。分批收貨保留剩餘在途庫存。|Brouillon → expédition → transit → réception. Les réceptions partielles conservent le reste du stock en transit.
The full transfer quantity will move into unavailable in-transit stock.|全部调拨数量将移入不可用的在途库存。|全部調撥數量將移入不可用的在途庫存。|Toute la quantité transférée passera dans le stock en transit indisponible.
Quantity received now|本次收货数量|本次收貨數量|Quantité reçue maintenant
Dispatch transfer|发出调拨|發出調撥|Expédier le transfert
Receive transfer|接收调拨|接收調撥|Recevoir le transfert
New transfer|新建调拨|新增調撥|Nouveau transfert
Sent|已发出|已發出|Envoyé
Send return to supplier|发出供应商退货|發出供應商退貨|Expédier le retour fournisseur
FIFO dispatch book value|FIFO 发出账面价值|FIFO 發出帳面價值|Valeur comptable FIFO expédiée
Current product value at destination|目标仓库当前产品价值|目標倉庫目前產品價值|Valeur actuelle du produit à destination
Selected receipt controls supplier credit matching. Oldest available warehouse FIFO layers determine book cost.|所选收货记录用于供应商贷项匹配。仓库中最早可用 FIFO 成本层决定账面成本。|所選收貨記錄用於供應商貸項匹配。倉庫內最早可用 FIFO 成本層決定帳面成本。|La réception choisie détermine le rapprochement du crédit fournisseur. Les plus anciennes couches FIFO disponibles de l'entrepôt déterminent le coût comptable.
Receipt|收货记录|收貨記錄|Réception
Original receipt|原始收货记录|原始收貨記錄|Réception d'origine
Inventory journal|库存凭证|庫存憑證|Écriture de stock
Supplier credit|供应商贷项|供應商貸項|Crédit fournisseur
Movement|变动|變動|Mouvement
Transfer note|调拨备注|調撥備註|Note de transfert
Top 5 Products|前五名产品|前五名產品|Les 5 meilleurs produits
Top Products Chart|热门产品图表|熱門產品圖表|Graphique des meilleurs produits
▾ Top Products Chart|▾ 热门产品图表|▾ 熱門產品圖表|▾ Graphique des meilleurs produits
▸ Top Products Chart|▸ 热门产品图表|▸ 熱門產品圖表|▸ Graphique des meilleurs produits
Move Top Products Chart earlier|将热门产品图表前移|將熱門產品圖表前移|Déplacer le graphique des meilleurs produits avant
Move Top Products Chart later|将热门产品图表后移|將熱門產品圖表後移|Déplacer le graphique des meilleurs produits après
Resize Top Products Chart|调整热门产品图表大小|調整熱門產品圖表大小|Redimensionner le graphique des meilleurs produits
Remove Top Products Chart|移除热门产品图表|移除熱門產品圖表|Retirer le graphique des meilleurs produits
Net sales|销售净额|銷售淨額|Ventes nettes
Select a product for sales details.|选择产品查看销售明细。|選擇產品檢視銷售明細。|Sélectionnez un produit pour voir le détail des ventes.
No positive net sales in this year.|今年没有正销售净额。|今年沒有正銷售淨額。|Aucune vente nette positive cette année.
Back to invoices|返回销售发票|返回銷售發票|Retour aux factures clients
Back to supplier bills|返回供应商账单|返回供應商帳單|Retour aux factures fournisseurs
Back to credit notes|返回贷项通知单|返回貸項通知單|Retour aux avoirs
This document was not found in this section. Return to the list and choose a document.|在此模块中未找到此单据。请返回列表选择单据。|在此模組中未找到此單據。請返回清單選擇單據。|Ce document est introuvable dans cette section. Revenez à la liste et sélectionnez un document.
Deliveries & backorders|分批发货与欠交订单|分批出貨與欠交訂單|Livraisons et reliquats
Release shipment|释放本批发货|釋放本批出貨|Libérer une livraison
Backordered|待补发|待補發|En reliquat
Part shipped|部分已发货|部分已出貨|Partiellement expédié
Released|已释放|已釋放|Libéré
Each delivery retains its own quantities. The original sales order and prices stay unchanged.|每批发货单独记录数量，原销售订单与价格保持不变。|每批出貨單獨記錄數量，原銷售訂單與價格保持不變。|Chaque livraison conserve ses quantités. La commande initiale et ses prix restent inchangés.
Transfer freight costing|调拨运费核算|調撥運費核算|Coût du fret des transferts
Allocate transfer freight|分摊调拨运费|分攤調撥運費|Répartir le fret de transfert
Freight bill|运费账单|運費帳單|Facture de fret
Review allocation|审核分摊|審核分攤|Examiner la répartition
Review transfer freight|审核调拨运费|審核調撥運費|Examiner le fret de transfert
Retained / sold / other|留存 / 已售 / 其他|留存 / 已售 / 其他|En stock / vendu / autre
Future receipts are excluded.|不包含未来收货数量。|不包含未來收貨數量。|Les réceptions futures sont exclues.
Allocate an issued freight bill to received transfers. FIFO follows the received ranges; Average uses prospective exposure after full receipt. Future receipts are excluded.|将已开具的运费账单分摊至已收调拨。FIFO 按已收成本层；平均成本须全部收货后按前瞻敞口分摊。不包含未来收货。|將已開立的運費帳單分攤至已收調撥。FIFO 按已收成本層；平均成本須全部收貨後按前瞻曝險分攤。不包含未來收貨。|Répartissez une facture de fret émise entre les transferts reçus. FIFO suit les couches reçues; le coût moyen utilise l’exposition prospective après réception complète. Les réceptions futures sont exclues.
Use Sales Order → Release shipment to ship part now and retain the balance on the same order.|在销售订单中选择释放本批发货，余量保留在原订单中。|在銷售訂單中選擇釋放本批出貨，餘量保留在原訂單中。|Dans la commande client, libérez une livraison partielle; le solde reste sur la même commande.
Original shipment|原发货单|原出貨單|Livraison d’origine
Create return|创建退货单|建立退貨單|Créer un retour
Inventory still held|留存库存|留存庫存|Stock encore détenu
Goods already sold|已售货物|已售貨物|Marchandises déjà vendues
Write-offs|减记成本|減記成本|Coûts dépréciés
Journal|会计凭证|會計憑證|Écriture comptable
Transfers|调拨单|調撥單|Transferts
Received quantity|已收货数量|已收貨數量|Quantité reçue
Transfer freight allocated|调拨运费已分摊|調撥運費已分攤|Fret de transfert réparti
Delivery released|发货批次已释放|出貨批次已釋放|Livraison libérée
Create and issue a freight charge bill, and receive a warehouse transfer first.|请先创建并开具运费账单，再接收仓库调拨。|請先建立並開立運費帳單，再接收倉庫調撥。|Créez et émettez une facture de fret, puis recevez un transfert d’entrepôt.
Stock shortage|库存缺口|庫存缺口|Manque de stock
Scan to open|扫码打开|掃碼開啟|Scanner pour ouvrir
Document scanner|单据扫码器|單據掃碼器|Lecteur de documents
Document barcode or QR|单据条码或二维码|單據條碼或 QR 碼|Code-barres ou QR du document
Open document|打开单据|開啟單據|Ouvrir le document
Start camera|启动相机|啟動相機|Démarrer la caméra
Stop camera|停止相机|停止相機|Arrêter la caméra
Take photo / choose image|拍照 / 选择图片|拍照 / 選擇圖片|Prendre une photo / choisir une image
Open on phone|手机打开|手機開啟|Ouvrir sur téléphone
Scan in Harbor|在 Harbor 中扫码|在 Harbor 中掃碼|Scanner dans Harbor
Document found.|已找到单据。|已找到單據。|Document trouvé.
Ready to scan. No records are changed.|可以扫码。不会更改单据。|可以掃碼。不會變更單據。|Prêt à scanner. Aucun dossier n’est modifié.
Keep the whole barcode or QR inside the camera view.|请将完整条码或二维码放在取景框内。|請將完整條碼或 QR 碼放在取景框內。|Gardez le code-barres ou le QR entier dans le champ de la caméra.
Camera ready. Point at a document barcode or QR.|相机已启动，请对准单据条码或二维码。|相機已啟動，請對準單據條碼或 QR 碼。|Caméra prête. Visez le code-barres ou le QR d’un document.
Camera images are decoded on this device. Scanning a document does not change stock or accounting.|相机图片仅在此设备上解码。扫码打开单据不会更改库存或账务。|相機圖片僅在此裝置上解碼。掃碼開啟單據不會變更庫存或帳務。|Les images sont décodées sur cet appareil. Scanner un document ne modifie ni le stock ni la comptabilité.
Read-only document. No stock or accounting changed.|单据仅供查看。库存与账务未更改。|單據僅供檢視。庫存與帳務未變更。|Document en lecture seule. Stock et comptabilité inchangés.
Phone camera setup|手机相机设置|手機相機設定|Configuration de la caméra du téléphone
Phone setup steps|手机设置步骤|手機設定步驟|Étapes de configuration du téléphone
Phone document scanner|手机单据扫码|手機單據掃碼|Lecteur de documents sur téléphone
Open phone document scanner|打开手机单据扫码器|開啟手機單據掃碼器|Ouvrir le lecteur de documents du téléphone
Set phone address for QR codes|设置二维码手机地址|設定 QR 碼手機位址|Définir l’adresse du téléphone pour les QR
Phone HTTPS address|手机 HTTPS 地址|手機 HTTPS 位址|Adresse HTTPS du téléphone
Save address|保存地址|儲存位址|Enregistrer l’adresse
Phone address is saved for printing. The phone gateway must still be running.|已保存打印用手机地址，手机网关仍需保持运行。|已儲存列印用手機位址，手機閘道仍需保持執行。|L’adresse du téléphone est enregistrée pour l’impression. La passerelle doit rester ouverte.
Phone address is not configured. QR codes can still be read inside the Harbor scanner.|尚未设置手机地址。仍可在 Harbor 扫码器中读取二维码。|尚未設定手機位址。仍可在 Harbor 掃碼器中讀取 QR 碼。|L’adresse du téléphone n’est pas configurée. Les QR restent lisibles dans le lecteur Harbor.
Live camera needs a trusted HTTPS address and a Harbor login. Photo decoding works without BarcodeDetector.|实时相机需要可信 HTTPS 地址和 Harbor 登录。照片解码无需 BarcodeDetector。|即時相機需要可信 HTTPS 位址和 Harbor 登入。照片解碼無需 BarcodeDetector。|La caméra en direct nécessite une adresse HTTPS de confiance et une connexion Harbor. Le décodage photo fonctionne sans BarcodeDetector.
Live camera needs trusted HTTPS on phones. Use Take photo / choose image, or follow Phone setup.|手机实时相机需要可信 HTTPS。请使用拍照 / 选择图片，或按照手机设置步骤操作。|手機即時相機需要可信 HTTPS。請使用拍照 / 選擇圖片，或按照手機設定步驟操作。|La caméra en direct nécessite HTTPS de confiance. Utilisez une photo ou suivez la configuration du téléphone.
Use the trusted HTTPS address shown by Start Harbor Mobile. Saving an address does not start remote access.|请输入 Start Harbor Mobile 显示的可信 HTTPS 地址。保存地址不会启用远程访问。|請輸入 Start Harbor Mobile 顯示的可信 HTTPS 位址。儲存位址不會啟用遠端存取。|Utilisez l’adresse HTTPS de confiance affichée par Start Harbor Mobile. L’enregistrement n’active pas l’accès distant.
Open invoices, purchase orders and shipments without changing warehouse records.|打开销售发票、采购订单与发货单，不更改仓库记录。|開啟銷售發票、採購訂單與出貨單，不變更倉庫記錄。|Ouvrez factures, commandes fournisseurs et expéditions sans modifier les dossiers.
Scan to open documents|扫码打开单据|掃碼開啟單據|Scanner pour ouvrir des documents
Camera permission was denied. Allow camera access in your browser settings, or use a photo.|相机权限被拒绝。请在浏览器设置中允许相机，或使用照片。|相機權限遭拒。請在瀏覽器設定中允許相機，或使用照片。|Accès caméra refusé. Autorisez la caméra dans le navigateur ou utilisez une photo.
Camera could not start. Use Take photo / choose image.|相机无法启动。请使用拍照 / 选择图片。|相機無法啟動。請使用拍照 / 選擇圖片。|La caméra n’a pas démarré. Utilisez une photo ou une image.
Reading image…|正在读取图片…|正在讀取圖片…|Lecture de l’image…
Choose an image smaller than 20 MB.|请选择小于 20 MB 的图片。|請選擇小於 20 MB 的圖片。|Choisissez une image de moins de 20 Mo.
This image could not be opened. Try a JPEG or PNG photo.|无法打开此图片。请使用 JPEG 或 PNG 照片。|無法開啟此圖片。請使用 JPEG 或 PNG 照片。|Cette image ne s’ouvre pas. Essayez une photo JPEG ou PNG.
No readable barcode found. Move closer, improve lighting or choose a sharper photo.|未找到可读条码。请靠近一些、改善光线或选择更清晰的照片。|未找到可讀條碼。請靠近一些、改善光線或選擇更清晰的照片。|Aucun code lisible. Rapprochez-vous, améliorez l’éclairage ou choisissez une photo plus nette.
Scan an invoice, purchase order or shipment document number.|请扫描发票、采购订单或发货单编号。|請掃描發票、採購訂單或出貨單編號。|Scannez un numéro de facture, de commande fournisseur ou d’expédition.
Document not found. Refresh Harbor and check the printed number.|未找到单据。请刷新 Harbor 并核对打印编号。|未找到單據。請重新整理 Harbor 並核對列印編號。|Document introuvable. Actualisez Harbor et vérifiez le numéro imprimé.
Document number is ambiguous. Choose the record manually.|单据编号不唯一。请手动选择记录。|單據編號不唯一。請手動選擇記錄。|Numéro de document ambigu. Sélectionnez le dossier manuellement.
This QR link belongs to another site. Enter the Harbor document number instead.|此二维码链接属于其他网站。请直接输入 Harbor 单据编号。|此 QR 碼連結屬於其他網站。請直接輸入 Harbor 單據編號。|Ce QR pointe vers un autre site. Saisissez le numéro du document Harbor.
Use a trusted HTTPS phone address on your private network.|请使用私有网络中可信的 HTTPS 手机地址。|請使用私有網路中可信的 HTTPS 手機位址。|Utilisez une adresse HTTPS de confiance sur votre réseau privé.
Scanned text is too long.|扫码文本过长。|掃碼文字過長。|Le texte scanné est trop long.
Invalid document link.|单据链接无效。|單據連結無效。|Lien de document incorrect.
Sign in and load the shared workspace first.|请先登录并加载共享工作区。|請先登入並載入共用工作區。|Connectez-vous et chargez d’abord l’espace partagé.
Grouped picking|分组拣货|分組揀貨|Prélèvement groupé
Pick group|拣货组|揀貨組|Groupe de prélèvement
Create grouped pick|创建分组拣货|建立分組揀貨|Créer un prélèvement groupé
Choose 2–20 uncommitted picks in one warehouse and owner.|请选择同一仓库和货主的 2–20 个未预留拣货单。|請選擇同一倉庫和貨主的 2–20 個未預留揀貨單。|Choisissez 2 à 20 prélèvements non réservés du même entrepôt et propriétaire.
Each tote belongs to one customer order. Original quantities and costs stay unchanged.|每个周转箱对应一张客户订单，原始数量和成本保持不变。|每個周轉箱對應一張客戶訂單，原始數量和成本保持不變。|Chaque bac correspond à une commande client. Les quantités et coûts d’origine sont conservés.
Prepare order totes|准备订单周转箱|準備訂單周轉箱|Préparer les bacs de commande
Reserve group|预留整组库存|預留整組庫存|Réserver le groupe
Combined pick list|合并拣货清单|合併揀貨清單|Liste de prélèvement combinée
Order tote barcode|订单周转箱条码|訂單周轉箱條碼|Code-barres du bac de commande
Source bin barcode|来源库位条码|來源儲位條碼|Code-barres de l’emplacement source
Save tote scan|保存周转箱扫描|儲存周轉箱掃描|Enregistrer le scan du bac
Finish scanned group|完成分组扫描拣货|完成分組掃描揀貨|Terminer le prélèvement groupé scanné
Grouped picking finished. Open Packing for each shipment.|分组拣货已完成，请分别打开各发货单进行装箱。|分組揀貨已完成，請分別開啟各出貨單進行裝箱。|Prélèvement groupé terminé. Ouvrez l’emballage de chaque expédition.
Print tote and bin barcodes|打印周转箱和库位条码|列印周轉箱與儲位條碼|Imprimer les codes des bacs et emplacements
Start scanned packing|开始扫描装箱|開始掃描裝箱|Commencer l’emballage scanné
Carton name|纸箱名称|紙箱名稱|Nom du carton
Add scan carton|添加扫描纸箱|新增掃描紙箱|Ajouter un carton à scanner
Carton barcode|纸箱条码|紙箱條碼|Code-barres du carton
Save carton scan|保存纸箱扫描|儲存紙箱掃描|Enregistrer le scan du carton
Seal scanned packing|确认并封箱|確認並封箱|Valider et fermer les cartons
Carrier / local delivery|承运商或本地配送|承運商或本地配送|Transporteur ou livraison locale
Tracking reference|物流跟踪编号|物流追蹤編號|Référence de suivi
Carrier service|配送服务|配送服務|Service du transporteur
I reviewed quantities and the selected shipment.|我已核对数量和所选发货单。|我已核對數量與所選出貨單。|J’ai vérifié les quantités et l’expédition sélectionnée.
Reviewed cartons|已核对纸箱|已核對紙箱|Cartons vérifiés
Shipment barcode|发货单条码|出貨單條碼|Code-barres de l’expédition
Carton barcodes (one per line)|纸箱条码（每行一个）|紙箱條碼（每行一個）|Codes-barres des cartons (un par ligne)
Dispatch reviewed shipment|确认核对并发货|確認核對並出貨|Expédier après vérification
Print carton barcodes|打印纸箱条码|列印紙箱條碼|Imprimer les codes des cartons
This shipment needs scanned packing before mobile dispatch.|手机发货前必须完成扫描装箱。|手機出貨前必須完成掃描裝箱。|Cette expédition nécessite un emballage scanné avant l’envoi mobile.
Reset reason|重置原因|重設原因|Motif de réinitialisation
Reset scanned packing|重置扫描装箱|重設掃描裝箱|Réinitialiser l’emballage scanné
Changes save to the shared warehouse. No carrier booking or postage purchase.|更改将保存到共享仓库，不会预订承运商或购买运单。|變更將儲存至共用倉庫，不會預訂承運商或購買運單。|Les modifications sont enregistrées dans l’entrepôt partagé. Aucune réservation ni aucun affranchissement n’est acheté.
Print at actual size. Warehouse labels are not postage.|请按实际大小打印。仓库标签并非邮资标签。|請按實際大小列印。倉庫標籤並非郵資標籤。|Imprimez à taille réelle. Les étiquettes d’entrepôt ne constituent pas un affranchissement.
No matching work in this warehouse.|此仓库没有符合条件的工作。|此倉庫沒有符合條件的工作。|Aucune tâche correspondante dans cet entrepôt.
Print warehouse labels|打印仓库标签|列印倉庫標籤|Imprimer les étiquettes d’entrepôt
Scan already recorded. Refresh and review the saved quantity.|扫描已保存，请刷新并核对数量。|掃描已儲存，請重新整理並核對數量。|Scan déjà enregistré. Actualisez et vérifiez la quantité enregistrée.
Tote barcode does not belong to this group.|周转箱条码不属于此组。|周轉箱條碼不屬於此組。|Ce bac n’appartient pas à ce groupe.
Product, lot or source bin does not match this order.|产品、批次或来源库位与订单不符。|產品、批次或來源儲位與訂單不符。|Le produit, le lot ou l’emplacement ne correspond pas à la commande.
Scanned quantity exceeds the remaining allocation.|扫描数量超过剩余分配数量。|掃描數量超過剩餘分配數量。|La quantité scannée dépasse l’allocation restante.
Carton barcode does not belong to this shipment.|纸箱条码不属于此发货单。|紙箱條碼不屬於此出貨單。|Ce carton n’appartient pas à cette expédition.
Shipment barcode does not match.|发货单条码不匹配。|出貨單條碼不符。|Le code de l’expédition ne correspond pas.
Scan every carton exactly once before dispatch.|发货前请将每个纸箱恰好扫描一次。|出貨前請將每個紙箱恰好掃描一次。|Scannez chaque carton une seule fois avant l’expédition.
Review and scan every unit; each carton must contain stock.|请核对并扫描每件产品，每个纸箱必须包含库存。|請核對並掃描每件產品，每個紙箱必須包含庫存。|Vérifiez et scannez chaque unité. Chaque carton doit contenir du stock.
Scan every allocated unit into its order tote before finishing.|完成前请将每件已分配产品扫描到对应订单周转箱。|完成前請將每件已分配產品掃描至對應訂單周轉箱。|Scannez toutes les unités attribuées dans le bac de leur commande avant de terminer.
Tote scan saved|周转箱扫描已保存|周轉箱掃描已儲存|Scan du bac enregistré
Scan carton added|扫描纸箱已添加|掃描紙箱已新增|Carton ajouté
Carton scan saved|纸箱扫描已保存|紙箱掃描已儲存|Scan du carton enregistré
Scanned packing opened|扫描装箱已打开|掃描裝箱已開啟|Emballage scanné ouvert
Scanned packing sealed|扫描装箱已封箱|掃描裝箱已封箱|Emballage scanné fermé
Scan group prepared|扫描组已准备|掃描組已準備|Groupe scanné préparé
Scan group reserved|扫描组库存已预留|掃描組庫存已預留|Groupe scanné réservé
Grouped picking finished|分组拣货已完成|分組揀貨已完成|Prélèvement groupé terminé
Saved.|已保存。|已儲存。|Enregistré.
Nothing was automatically retried. Review the current record before scanning again.|系统没有自动重试，请核对当前记录后再扫描。|系統沒有自動重試，請核對目前記錄後再掃描。|Aucune nouvelle tentative automatique. Vérifiez le dossier avant de scanner à nouveau.
Use barcode|使用条码|使用條碼|Utiliser le code-barres
The camera fills the selected field. Review quantities and save the scan to update the warehouse.|相机将填写所选字段，请核对数量并保存扫描以更新仓库。|相機將填寫所選欄位，請核對數量並儲存掃描以更新倉庫。|La caméra remplit le champ sélectionné. Vérifiez les quantités et enregistrez le scan pour mettre à jour l’entrepôt.
One serial per line|每行一个序列号|每行一個序號|Un numéro de série par ligne
Scan labels|扫描标签|掃描標籤|Étiquettes à scanner
Account menu|账户菜单|帳戶選單|Menu du compte
Checking sign-in…|正在检查登录状态…|正在檢查登入狀態…|Vérification de la connexion…
Session expired|登录已过期|登入已過期|Session expirée
Your session expired. Sign in again to continue.|您的登录已过期，请重新登录以继续。|您的登入已過期，請重新登入以繼續。|Votre session a expiré. Reconnectez-vous pour continuer.
Signed in as|当前登录账户|目前登入帳戶|Connecté en tant que
Create an administrator account to enable sign-in.|创建管理员账户以启用登录。|建立管理員帳戶以啟用登入。|Créez un compte administrateur pour activer la connexion.
After signing in, you will return to this page. No failed action is automatically retried.|登录后将返回此页面，失败的操作不会自动重试。|登入後將返回此頁面，失敗的操作不會自動重試。|Après connexion, vous reviendrez sur cette page. Aucune action échouée n’est relancée automatiquement.
Use Sign in at the top right to open the shared workspace.|点击右上角的登录以打开共享工作区。|點選右上角的登入以開啟共用工作區。|Utilisez Connexion en haut à droite pour ouvrir l’espace partagé.
Sign in with the account control at the top right.|请使用右上角的账户菜单登录。|請使用右上角的帳戶選單登入。|Connectez-vous depuis le menu du compte en haut à droite.
Sign in to the shared workspace.|请登录共享工作区。|請登入共用工作區。|Connectez-vous à l’espace partagé.
Administrator|管理员|管理員|Administrateur
Viewer|只读用户|唯讀使用者|Lecteur
`;

