import {receivingCatalogue} from './locale-receiving.mjs';
import {workflowCatalogue} from './locale-workflow.mjs';
import {securityCatalogue} from './locale-security.mjs';
import {extraRows} from './locale-extra.mjs';
import {unitRows} from './locale-units.mjs';
import {salesRows} from './locale-sales.mjs';
import {crmRows} from './locale-crm.mjs';
import {productionRows} from './locale-production.mjs';
// Original Harbor translations. Keys describe presentation, never stored records.
const rows=`
Language|语言|語言|Langue
Currency|币种|幣別|Devise
Exchange rate|汇率|匯率|Taux de change
Stock units|库存单位|庫存單位|Unités de stock
Home value|本币金额|本幣金額|Valeur en devise locale
Receive|收货|收貨|Recevoir
Pick|拣货|揀貨|Préparer
Count|盘点|盤點|Compter
Warehouse scanning|仓库扫码|倉庫掃碼|Lecture de codes d’entrepôt
Mobile warehouse|移动仓库|行動倉庫|Entrepôt mobile
Connecting to Harbor…|正在连接 Harbor…|正在連接 Harbor…|Connexion à Harbor…
Committed pick|已分配拣货单|已分配揀貨單|Préparation affectée
Stock row|库存行|庫存列|Ligne de stock
Receive into|收货库位|收貨庫位|Réceptionner dans
Expiry date|到期日|到期日|Date d’expiration
Delivery reference|收货参考编号|收貨參考編號|Référence de livraison
Count reason|盘点原因|盤點原因|Motif du comptage
Barcode or SKU|条码或 SKU|條碼或 SKU|Code-barres ou SKU
Camera|相机|相機|Caméra
Actual counted quantity|实际盘点数量|實際盤點數量|Quantité réellement comptée
Save scan|保存扫码|儲存掃碼|Enregistrer la lecture
Save count|保存盘点|儲存盤點|Enregistrer le comptage
Finish scanned pick|完成扫码拣货|完成掃碼揀貨|Terminer la préparation scannée
Serial numbers, if tracked|序列号（如需追踪）|序號（如需追蹤）|Numéros de série, si suivis
One serial per line|每行一个序列号|每行一個序號|Un numéro de série par ligne
Scan a barcode|扫描条码|掃描條碼|Lire un code-barres
Close camera|关闭相机|關閉相機|Fermer la caméra
Interface language|界面语言|介面語言|Langue de l’interface
Skip to workspace|跳转到工作区|跳至工作區|Aller à l’espace de travail
Close navigation|关闭导航|關閉導覽|Fermer la navigation
Toggle navigation|切换导航|切換導覽|Afficher la navigation
Workspace|工作区|工作區|Espace de travail
Overview|概览|概覽|Vue d’ensemble
Inventory|库存|庫存|Stocks
Purchasing|采购|採購|Achats
Sales|销售|銷售|Ventes
Manufacturing|生产制造|生產製造|Fabrication
Accounting|会计|會計|Comptabilité
Reports & dashboards|报表与仪表板|報表與儀表板|Rapports et tableaux de bord
Setup & integrations|设置与集成|設定與整合|Configuration et intégrations
Products & stock|产品与库存|產品與庫存|Produits et stocks
FIFO cost layers|FIFO 成本层|FIFO 成本層|Couches de coûts FIFO
Product rules|产品规则|產品規則|Règles des produits
Replenishment|补货|補貨|Réapprovisionnement
Transfer orders|调拨单|調撥單|Ordres de transfert
Cycle counts|循环盘点|循環盤點|Inventaires tournants
Traceability & recalls|追溯与召回|追溯與召回|Traçabilité et rappels
Barcode station|条码工作站|條碼工作站|Station de codes-barres
Purchase orders|采购订单|採購訂單|Commandes fournisseurs
Suppliers|供应商|供應商|Fournisseurs
Purchasing approvals|采购审批|採購審批|Approbations des achats
Receiving & putaway|收货与上架|收貨與上架|Réception et rangement
Supplier prices & currency|供应商价格与币种|供應商價格與幣別|Prix fournisseurs et devises
Purchase cost reconciliation|采购成本核对|採購成本核對|Rapprochement des coûts d’achat
Supplier returns|供应商退货|供應商退貨|Retours fournisseurs
Sales orders|销售订单|銷售訂單|Commandes clients
Customers & pricing|客户与定价|客戶與定價|Clients et tarification
Kits & bundles|套件与组合|套件與組合|Kits et ensembles
Picking|拣货|揀貨|Préparation
Shipping|发货|出貨|Expédition
Customer returns|客户退货|客戶退貨|Retours clients
BOMs & work orders|物料清单与工单|物料清單與工單|Nomenclatures et ordres de fabrication
Invoices|发票|發票|Factures clients
Supplier bills|供应商账单|供應商帳單|Factures fournisseurs
Credit notes|贷项通知单|貸項通知單|Notes de crédit
Payments & balances|付款与余额|付款與餘額|Paiements et soldes
Inventory journals|库存会计凭证|庫存會計憑證|Écritures de stock
Inventory reconciliation|库存对账|庫存對帳|Rapprochement des stocks
Historical valuation|历史估值|歷史估值|Évaluation historique
Dashboards|仪表板|儀表板|Tableaux de bord
Business dashboard|业务仪表板|業務儀表板|Tableau de bord de l’entreprise
Demand forecasting|需求预测|需求預測|Prévision de la demande
Report centre|报表中心|報表中心|Centre de rapports
Activity history|活动历史|活動歷史|Historique des activités
Activity|活动|活動|Activités
Locations|库位|庫位|Emplacements
Warehouses & owners|仓库与货主|倉庫與貨主|Entrepôts et propriétaires
QuickBooks sandbox|QuickBooks 沙盒|QuickBooks 沙盒|Bac à sable QuickBooks
Partner exchange|合作伙伴交换|合作夥伴交換|Échanges partenaires
Users & backups|用户与备份|使用者與備份|Utilisateurs et sauvegardes
Data & settings|数据与设置|資料與設定|Données et paramètres
Primary location · Demo|主库位 · 示例|主庫位 · 範例|Emplacement principal · Démo
Your working sandbox|您的测试工作区|您的測試工作區|Votre espace d’essai
Explore the warehouse with sample stock and real workflows.|使用示例库存体验仓库流程。|使用範例庫存體驗倉庫流程。|Explorez l’entrepôt avec des stocks de démonstration et des flux réels.
Local workspace|本地工作区|本機工作區|Espace de travail local
Not signed in|尚未登录|尚未登入|Non connecté
Admin|管理员|管理員|Administrateur
Accounting role|会计角色|會計角色|Rôle comptable
Interface|界面|介面|Interface
Classic workspace|经典工作区|經典工作區|Espace classique
Harbor modern|Harbor 现代风格|Harbor 現代風格|Harbor moderne
Shared local database|共享本地数据库|共用本機資料庫|Base de données locale partagée
Connection needs attention|连接需要处理|連線需要處理|Connexion à vérifier
Choose workspace|选择工作区|選擇工作區|Choisir l’espace de travail
PROTOTYPE|原型|原型|PROTOTYPE
Open walkthrough|打开操作指南|開啟操作指南|Ouvrir le guide
Independent prototype · Shared data on this computer|独立原型 · 数据共享在此电脑上|獨立原型 · 資料共用於此電腦|Prototype indépendant · Données partagées sur cet ordinateur
A clear view of your warehouse.|清晰掌握仓库情况。|清楚掌握倉庫狀況。|Une vue claire de votre entrepôt.
Keep stock moving, from the receiving dock to the customer.|让库存从收货区顺畅流向客户。|讓庫存從收貨區順暢流向客戶。|Faites circuler les stocks, de la réception jusqu’au client.
Receive stock|接收库存|接收庫存|Recevoir des stocks
New order|新建订单|新增訂單|Nouvelle commande
On-hand quantity|现有库存数量|現有庫存數量|Quantité en stock
Open orders|未完成订单|未完成訂單|Commandes ouvertes
Ready to ship|待发货|待出貨|Prêt à expédier
Low-stock items|低库存产品|低庫存產品|Produits à stock faible
All items above reorder point|所有产品均高于补货点|所有產品均高於補貨點|Tous les produits dépassent le seuil de réapprovisionnement
Review availability and replenish|检查可用数量并补货|檢查可用數量並補貨|Vérifier la disponibilité et réapprovisionner
Order queue|订单队列|訂單佇列|File des commandes
Your next customer orders, ready for action.|下一批客户订单，等待处理。|下一批客戶訂單，等待處理。|Vos prochaines commandes clients à traiter.
All orders|所有订单|所有訂單|Toutes les commandes
Inventory at a glance|库存概览|庫存概覽|Aperçu des stocks
Availability accounts for open demand and held stock.|可用数量已考虑未完成需求和冻结库存。|可用數量已考慮未完成需求和凍結庫存。|La disponibilité tient compte de la demande ouverte et des stocks bloqués.
View inventory|查看库存|查看庫存|Voir les stocks
Take it for a spin|试用流程|試用流程|Essayez le processus
Your first shipment|您的第一批发货|您的第一批出貨|Votre première expédition
starts here.|从这里开始。|從這裡開始。|commence ici.
Open the demo order|打开示例订单|開啟範例訂單|Ouvrir la commande de démonstration
On the floor|仓库现场|倉庫現場|Dans l’entrepôt
Work waiting in your warehouse.|仓库中等待处理的任务。|倉庫中等待處理的工作。|Tâches en attente dans votre entrepôt.
Picks to work|待拣货任务|待揀貨工作|Préparations à traiter
Reserve and stage stock|预留并暂存库存|預留並暫存庫存|Réserver et préparer les stocks
Shipments to dispatch|待派送货物|待派送貨物|Expéditions à envoyer
Pack, check, and ship|包装、检查并发货|包裝、檢查並出貨|Emballer, vérifier et expédier
Reserved quantity|预留数量|預留數量|Quantité réservée
Committed to active picks|已分配至当前拣货|已分配至目前揀貨|Affecté aux préparations actives
Recent activity|最近活动|最近活動|Activités récentes
All|全部|全部|Tous
Open|未完成|未完成|Ouvert
Closed|已关闭|已關閉|Fermé
Cancelled|已取消|已取消|Annulé
Draft|草稿|草稿|Brouillon
Issued|已下单|已下單|Émis
Picking|拣货|揀貨|Préparation
Picked|已拣货|已揀貨|Préparé
Fulfilled|已履行|已履行|Exécuté
Entered|已录入|已錄入|Saisi
Packed|已包装|已包裝|Emballé
Shipped|已发货|已出貨|Expédié
Committed|已分配|已分配|Affecté
Reserved|已预留|已預留|Réservé
Finished|已完成|已完成|Terminé
Ready|可用|可用|Prêt
Low|偏低|偏低|Faible
Pending approval|待审批|待審批|En attente d’approbation
Approved|已批准|已批准|Approuvé
Rejected|已退回|已退回|Refusé
Partially received|部分收货|部分收貨|Réception partielle
Received|已收货|已收貨|Reçu
Requested|已申请|已申請|Demandé
Completed|已完成|已完成|Terminé
Restock|重新入库|重新入庫|Remettre en stock
Scrap|报废|報廢|Mettre au rebut
Voided|已作废|已作廢|Annulé
Paid|已付清|已付清|Payé
Part paid|部分付款|部分付款|Partiellement payé
Credited|已抵扣|已抵扣|Crédité
Refund due|待退款|待退款|Remboursement dû
Credit issued|贷项已开立|貸項已開立|Crédit émis
Synced|已同步|已同步|Synchronisé
Ready for review|待审核|待審核|Prêt pour vérification
Reviewed|已审核|已審核|Vérifié
Failed|失败|失敗|Échec
Not configured|尚未配置|尚未設定|Non configuré
Not connected|未连接|未連線|Non connecté
Connected|已连接|已連線|Connecté
Save|保存|儲存|Enregistrer
Save details|保存详情|儲存詳細資料|Enregistrer les détails
Cancel|取消|取消|Annuler
Done|完成|完成|Terminé
Close dialog|关闭对话框|關閉對話框|Fermer la fenêtre
Create|创建|建立|Créer
Edit|编辑|編輯|Modifier
Delete|删除|刪除|Supprimer
Remove|移除|移除|Retirer
Search|搜索|搜尋|Rechercher
Refresh|刷新|重新整理|Actualiser
View|查看|檢視|Voir
Details|详情|詳細資料|Détails
General|常规|一般|Général
Memo|备注|備註|Mémo
Costing|成本|成本|Coûts
Custom|自定义|自訂|Personnalisé
Tracking|追踪|追蹤|Suivi
Move|移动|移動|Déplacer
Cycle|盘点|盤點|Compter
Issue|下单|下單|Émettre
Commit|分配|分配|Affecter
Finish|完成|完成|Terminer
Pack|包装|包裝|Emballer
Ship|发货|出貨|Expédier
Void pick|作废拣货|作廢揀貨|Annuler la préparation
Void shipment|作废发货|作廢出貨|Annuler l’expédition
Print|打印|列印|Imprimer
Export|导出|匯出|Exporter
Import|导入|匯入|Importer
Export CSV|导出 CSV|匯出 CSV|Exporter CSV
Import CSV|导入 CSV|匯入 CSV|Importer CSV
Download PDF|下载 PDF|下載 PDF|Télécharger le PDF
Preparing PDF…|正在生成 PDF…|正在產生 PDF…|Préparation du PDF…
Print preview|打印预览|列印預覽|Aperçu avant impression
Apply language|应用语言|套用語言|Appliquer la langue
Document language|单据语言|單據語言|Langue du document
Document language / 文档语言 / 文件語言|单据语言|單據語言|Langue du document
Report language|报表语言|報表語言|Langue du rapport
Document preview / 单据预览 / 單據預覽|单据预览|單據預覽|Aperçu du document
Billing preview / 单据预览 / 單據預覽|账务单据预览|帳務單據預覽|Aperçu de la facturation
Report preview / 报表预览 / 報表預覽|报表预览|報表預覽|Aperçu du rapport
Preview / PDF / 中文|预览 / PDF|預覽 / PDF|Aperçu / PDF
Historical valuation / 历史估值 / 歷史估值|历史估值|歷史估值|Évaluation historique
Inventory reconciliation / 库存对账 / 庫存對帳|库存对账|庫存對帳|Rapprochement des stocks
Item|产品|產品|Produit
Product|产品|產品|Produit
Products|产品|產品|Produits
Description|产品说明|產品說明|Description
Description / 说明 / 說明|产品说明|產品說明|Description
Item name|产品名称|產品名稱|Nom du produit
Product description|产品说明|產品說明|Description du produit
Category|类别|類別|Catégorie
Preferred supplier|首选供应商|首選供應商|Fournisseur préféré
Stock unit|库存单位|庫存單位|Unité de stock
Each|个|個|Unité
Roll|卷|卷|Rouleau
Pair|双|雙|Paire
Case|箱|箱|Caisse
Quantity|数量|數量|Quantité
Qty|数量|數量|Qté
Units|数量|數量|Unités
UOM|计量单位|計量單位|Unité
SKU|SKU|SKU|SKU
Name|名称|名稱|Nom
Number|编号|編號|Numéro
Order|订单|訂單|Commande
Customer|客户|客戶|Client
Supplier|供应商|供應商|Fournisseur
Customer / supplier|客户 / 供应商|客戶 / 供應商|Client / fournisseur
Status|状态|狀態|État
Due|到期|到期|Échéance
Due date|到期日|到期日|Date d’échéance
Unscheduled|未排期|未排程|Non planifié
Reference|参考编号|參考編號|Référence
Reference (optional)|参考编号（可选）|參考編號（選填）|Référence (facultatif)
Location|库位|庫位|Emplacement
Warehouse|仓库|倉庫|Entrepôt
Owner|货主|貨主|Propriétaire
On hand|现有库存|現有庫存|En stock
On Hand|现有库存|現有庫存|En stock
Available|可用|可用|Disponible
Stock level|库存水平|庫存水準|Niveau de stock
Reorder Point|补货点|補貨點|Seuil de réapprovisionnement
Reorder point|补货点|補貨點|Seuil de réapprovisionnement
Available To Pick|可拣货数量|可揀貨數量|Disponible à préparer
Information|信息|資訊|Informations
Line Count|行数|行數|Nombre de lignes
Display UOM|显示单位|顯示單位|Unité affichée
On Order|采购在途|採購在途|En commande
Stock by location|各库位库存|各庫位庫存|Stock par emplacement
Record activity|记录活动|記錄活動|Activité du dossier
Time|时间|時間|Heure
Action|操作|操作|Action
Note|备注|備註|Note
Notes|备注|備註|Notes
New inventory item|新建库存产品|新增庫存產品|Nouveau produit en stock
New item|新建产品|新增產品|Nouveau produit
Create item|创建产品|建立產品|Créer le produit
Edit product text|编辑产品文字|編輯產品文字|Modifier le texte du produit
New location|新建库位|新增庫位|Nouvel emplacement
Location code|库位代码|庫位代碼|Code d’emplacement
Location type|库位类型|庫位類型|Type d’emplacement
Destination|目标库位|目的庫位|Destination
Storage|存储区|儲存區|Stockage
Receiving|收货区|收貨區|Réception
Hold|质量冻结|品質凍結|Blocage qualité
Staging|暂存区|暫存區|Zone de préparation
Lot|批次|批次|Lot
Lot / batch|批次|批次|Lot
Expiry|到期日|到期日|Expiration
Serial numbers (one per line if tracked)|序列号（如追踪，每行一个）|序號（如追蹤，每行一個）|Numéros de série (un par ligne si suivis)
New purchase order|新建采购订单|新增採購訂單|Nouvelle commande fournisseur
Purchase order|采购订单|採購訂單|Commande fournisseur
Order products from suppliers and track each delivery.|向供应商订购产品并追踪交货。|向供應商訂購產品並追蹤交貨。|Commandez des produits aux fournisseurs et suivez chaque livraison.
Search purchase orders|搜索采购订单|搜尋採購訂單|Rechercher les commandes fournisseurs
Received / ordered|已收 / 已订|已收 / 已訂|Reçu / commandé
Open Chinese examples|打开中文示例|開啟中文範例|Ouvrir les exemples chinois
No purchase orders match this view.|没有符合此视图的采购订单。|沒有符合此檢視的採購訂單。|Aucune commande fournisseur ne correspond à cette vue.
Search suppliers|搜索供应商|搜尋供應商|Rechercher les fournisseurs
New supplier|新建供应商|新增供應商|Nouveau fournisseur
Supplier name|供应商名称|供應商名稱|Nom du fournisseur
Supplier address|供应商地址|供應商地址|Adresse du fournisseur
English name (optional)|英文名称（可选）|英文名稱（選填）|Nom anglais (facultatif)
Contact|联系方式|聯絡方式|Contact
Email|电子邮箱|電子郵件|Courriel
Phone|电话|電話|Téléphone
Address|地址|地址|Adresse
Payment terms|付款条件|付款條件|Conditions de paiement
Save supplier|保存供应商|儲存供應商|Enregistrer le fournisseur
Receive purchase|接收采购货物|接收採購貨物|Réceptionner la commande
Receive to hold|收货至质量冻结区|收貨至品質凍結區|Recevoir en zone de contrôle
Inspect / disposition|检验 / 处理|檢驗 / 處置|Inspecter / traiter
Return inspection result|退货检验结果|退貨檢驗結果|Résultat de l’inspection du retour
Receive return for inspection|接收退货进行检验|接收退貨進行檢驗|Recevoir le retour pour inspection
Quality hold|质量冻结区|品質凍結區|Blocage qualité
Disposition|处理方式|處置方式|Traitement
Units inspected now|本次检验数量|本次檢驗數量|Unités inspectées maintenant
Restock destination|重新入库库位|重新入庫庫位|Destination de remise en stock
Replacement order|补发订单|補發訂單|Commande de remplacement
Customer return|客户退货|客戶退貨|Retour client
Supplier return|供应商退货|供應商退貨|Retour fournisseur
Return|退货|退貨|Retour
Type|类型|類型|Type
Reason|原因|原因|Motif
Reason / 原因|原因|原因|Motif
Product / quantity|产品 / 数量|產品 / 數量|Produit / quantité
Accounting journal|会计凭证|會計憑證|Écriture comptable
Approval|审批|審批|Approbation
Approved - not issued|已批准 - 尚未下单|已批准 - 尚未下單|Approuvé - non émis
Captured book value|保存的账面价值|保存的帳面價值|Valeur comptable enregistrée
Captured snapshot|保存的估值快照|保存的估值快照|Instantané enregistré
Captured unit cost|保存的单位成本|保存的單位成本|Coût unitaire enregistré
Carrier / service|承运商 / 服务|承運商 / 服務|Transporteur / service
Carton|箱号|箱號|Colis
Checked|核对时间|核對時間|Vérifié
Checkpoint|检查点|檢查點|Point de contrôle
Checkpoint movement matched|检查点变动一致|檢查點變動一致|Variation du point de contrôle concordante
Costing method|成本方法|成本方法|Méthode de valorisation
Coverage starts|历史记录起点|歷史記錄起點|Début de l’historique
Credit note|贷项通知单|貸項通知單|Note de crédit
Current inventory|当前库存|目前庫存|Stock actuel
Custom fields|自定义字段|自訂欄位|Champs personnalisés
Delivery|交货方式|交貨方式|Livraison
Difference|差额|差額|Écart
Difference at checkpoint|检查点差额|檢查點差額|Écart au point de contrôle
Dimensions|尺寸|尺寸|Dimensions
Direct to customer|直送客户|直送客戶|Directement au client
Discount|折扣|折扣|Remise
Document date|单据日期|單據日期|Date du document
Draft - not issued|草稿 - 尚未下单|草稿 - 尚未下單|Brouillon - non émis
FIFO layer|FIFO 成本层|FIFO 成本層|Couche FIFO
Harbor inventory|Harbor 库存价值|Harbor 庫存價值|Valeur des stocks Harbor
Historical inventory valuation|历史库存估值|歷史庫存估值|Évaluation historique des stocks
Inventory book value returned|退货库存账面价值|退貨庫存帳面價值|Valeur comptable des stocks retournés
Issued credits|已开贷项|已開貸項|Crédits émis
Issued locally|已在本地下单|已在本地下單|Émis localement
Known QuickBooks inventory postings|已知 QuickBooks 库存入账|已知 QuickBooks 庫存入帳|Écritures de stock QuickBooks connues
Known value|已知价值|已知價值|Valeur connue
Local billing record. Payment entries record transactions made separately; they do not transfer money.|本地账务记录。付款记录登记另行完成的交易，不会转账。|本機帳務記錄。付款記錄登記另行完成的交易，不會轉帳。|Document de facturation local. Les paiements consignent des opérations effectuées séparément; ils ne transfèrent pas d’argent.
Local journal movement|本地库存凭证变动|本機庫存憑證變動|Variation des écritures locales
Local warehouse document. Currency is shown where specified. Not a tax invoice.|本地仓库单据。币种以单据标注为准。本单据不是税务发票。|本機倉庫單據。幣別以單據標註為準。本單據不是稅務發票。|Document d’entrepôt local. La devise est indiquée le cas échéant. Ce document n’est pas une facture fiscale.
Local warehouse label. NOT POSTAGE.|本地仓库标签，不含邮资。|本機倉庫標籤，不含郵資。|Étiquette d’entrepôt locale. NE VAUT PAS AFFRANCHISSEMENT.
Method / reference|方式 / 参考编号|方式 / 參考編號|Méthode / référence
Missing cost|缺失成本|缺失成本|Coût manquant
Movement since checkpoint|检查点后的变动|檢查點後的變動|Variation depuis le point de contrôle
Net amount|未税金额|未稅金額|Montant net
Order total|订单金额|訂單金額|Total de la commande
Our business|本公司|本公司|Notre entreprise
Outstanding|待收数量|待收數量|Restant
Outstanding balance|未付余额|未付餘額|Solde restant
Packing slip|装箱单|裝箱單|Bordereau de livraison
Page|页|頁|Page
Payment|付款|付款|Paiement
Payment history|付款历史|付款歷史|Historique des paiements
Payment instructions|付款说明|付款說明|Instructions de paiement
Payments recorded|已记录付款|已記錄付款|Paiements enregistrés
Pending approval - not issued|待审批 - 尚未下单|待審批 - 尚未下單|En attente d’approbation - non émis
Physical return|实物退货|實物退貨|Retour physique
Preserved snapshot. FIFO value is the remaining-layer sum. Earlier history is not reconstructed.|保存的历史快照。FIFO 价值为剩余成本层合计，不重建早期历史。|保存的歷史快照。FIFO 價值為剩餘成本層合計，不重建早期歷史。|Instantané conservé. La valeur FIFO est la somme des couches restantes. L’historique antérieur n’est pas reconstitué.
Purchase note|采购备注|採購備註|Note d’achat
Purchase revision|采购修订版本|採購修訂版本|Révision de la commande
QuickBooks inventory asset|QuickBooks 库存资产|QuickBooks 庫存資產|Actif des stocks QuickBooks
Read-only comparison. Warehouse values are local; QuickBooks is company-level. Historical differences are preserved.|只读比较。仓库价值来自本地；QuickBooks 为公司级账户。保留历史差额。|唯讀比較。倉庫價值來自本機；QuickBooks 為公司級帳戶。保留歷史差額。|Comparaison en lecture seule. Les valeurs d’entrepôt sont locales; QuickBooks couvre l’entreprise. Les écarts historiques sont conservés.
Recorded|已记录|已記錄|Enregistré
Reference / supplier invoice|参考编号 / 供应商发票号|參考編號 / 供應商發票號|Référence / facture fournisseur
Refund|退款|退款|Remboursement
Refunds recorded|已记录退款|已記錄退款|Remboursements enregistrés
Rejected - not issued|已退回 - 尚未下单|已退回 - 尚未下單|Refusé - non émis
Restocked units|已重新入库数量|已重新入庫數量|Unités remises en stock
Reversed|已冲销|已沖銷|Contrepassé
Review history|审核历史|審核歷史|Historique des vérifications
Review movement difference|请核查变动差额|請核查變動差額|Vérifier l’écart de variation
Sales invoice|销售发票|銷售發票|Facture de vente
Scrapped units|已报废数量|已報廢數量|Unités mises au rebut
Ship to|收货人|收貨人|Destinataire
Source|来源|來源|Source
Source document|来源单据|來源單據|Document source
Supplier bill record|供应商账单记录|供應商帳單記錄|Document de facture fournisseur
Supplier confirmation|供应商确认编号|供應商確認編號|Confirmation du fournisseur
Supplier credit net (home currency)|供应商贷项未税金额（本位币）|供應商貸項未稅金額（本位幣）|Crédit fournisseur net (devise locale)
Supplier credit record|供应商贷项记录|供應商貸項記錄|Document de crédit fournisseur
Supplier product code|供应商货号|供應商貨號|Code produit du fournisseur
Supplier-confirmed arrival|供应商确认到货日|供應商確認到貨日|Arrivée confirmée par le fournisseur
Tax|税额|稅額|Taxe
Tax registration|税务登记号|稅務登記號|Numéro d’inscription fiscale
To warehouse|送至仓库|送至倉庫|Vers l’entrepôt
Total|总额|總額|Total
Unexplained QuickBooks change|未解释的 QuickBooks 变动|未解釋的 QuickBooks 變動|Variation QuickBooks inexpliquée
Unexplained local change|未解释的本地变动|未解釋的本機變動|Variation locale inexpliquée
Unit cost|单位成本|單位成本|Coût unitaire
Unit price|单价|單價|Prix unitaire
Unrecovered cost difference|未收回成本差额|未收回成本差額|Écart de coût non récupéré
Unsynced inventory journals|未同步库存凭证|未同步庫存憑證|Écritures de stock non synchronisées
Warehouse label|仓库标签|倉庫標籤|Étiquette d’entrepôt
Warehouse stock values|仓库库存价值|倉庫庫存價值|Valeurs des stocks par entrepôt
Weight|重量|重量|Poids
continued|续页|續頁|suite
Weighted average|加权平均|加權平均|Moyenne pondérée
Average|平均|平均|Moyenne
Cost source|成本来源|成本來源|Source du coût
Labelled sample opening cost|标记的示例期初成本|標記的範例期初成本|Coût initial de démonstration identifié
Save labelled snapshot|保存命名快照|儲存命名快照|Enregistrer un instantané nommé
Start historical recording|开始记录历史|開始記錄歷史|Commencer l’historique
Apply filters|应用筛选|套用篩選|Appliquer les filtres
Export historical CSV|导出历史 CSV|匯出歷史 CSV|Exporter l’historique CSV
Preserved snapshot|保存的快照|保存的快照|Instantané conservé
Latest available / use date cutoff|最新快照 / 使用截止日期|最新快照 / 使用截止日期|Dernier disponible / date limite
As of (UTC)|截至时间（UTC）|截至時間（UTC）|À la date (UTC)
All owned warehouses|所有自有仓库|所有自有倉庫|Tous les entrepôts détenus
All products|所有产品|所有產品|Tous les produits
Valuation warehouse|估值仓库|估值倉庫|Entrepôt de valorisation
Valuation product|估值产品|估值產品|Produit de valorisation
Known inventory value|已知库存价值|已知庫存價值|Valeur connue des stocks
Owned units|自有库存数量|自有庫存數量|Unités détenues
Missing-cost products|缺失成本的产品|缺失成本的產品|Produits sans coût
Product / description|产品 / 说明|產品 / 說明|Produit / description
Method|方法|方法|Méthode
Captured FIFO layers|保存的 FIFO 成本层|保存的 FIFO 成本層|Couches FIFO enregistrées
Layer|成本层|成本層|Couche
Value|价值|價值|Valeur
Enable FIFO for a new product|为新产品启用 FIFO|為新產品啟用 FIFO|Activer FIFO pour un nouveau produit
Product / method|产品 / 方法|產品 / 方法|Produit / méthode
Next FIFO unit cost|下一件 FIFO 单位成本|下一件 FIFO 單位成本|Prochain coût unitaire FIFO
Remaining layer value|剩余成本层价值|剩餘成本層價值|Valeur des couches restantes
Receipt and return layers / 成本层 / 成本層|收货与退货成本层|收貨與退貨成本層|Couches de réception et de retour
Layer / source|成本层 / 来源|成本層 / 來源|Couche / source
Received / returned|收货 / 退货时间|收貨 / 退貨時間|Reçu / retourné
Remaining units|剩余数量|剩餘數量|Unités restantes
Remaining value|剩余价值|剩餘價值|Valeur restante
Receipt origin quantity / amount|原收货数量 / 金额|原收貨數量 / 金額|Quantité / montant de réception d’origine
Cost movements / 成本变动 / 成本變動|成本变动|成本變動|Mouvements de coûts
Movement / date|变动 / 日期|變動 / 日期|Mouvement / date
Source / kind|来源 / 类型|來源 / 類型|Source / type
Book value|账面价值|帳面價值|Valeur comptable
Slices|成本分配明细|成本分配明細|Détails d’affectation
Refresh comparison|刷新对账|重新整理對帳|Actualiser la comparaison
Record checkpoint|记录检查点|記錄檢查點|Enregistrer un point de contrôle
Export reconciliation CSV|导出对账 CSV|匯出對帳 CSV|Exporter le rapprochement CSV
Current company comparison|当前公司对账|目前公司對帳|Comparaison actuelle de l’entreprise
Inventory value|库存价值|庫存價值|Valeur des stocks
Preserved checkpoint|保存的检查点|保存的檢查點|Point de contrôle conservé
Movement since checkpoint / 检查点变动 / 檢查點變動|检查点后的变动|檢查點後的變動|Variation depuis le point de contrôle
Measure|指标|指標|Mesure
Starting values|期初价值|期初價值|Valeurs initiales
Actual movement|实际变动|實際變動|Variation réelle
Movement traced to journals / synced records|凭证 / 同步记录对应的变动|憑證 / 同步記錄對應的變動|Variation liée aux écritures / enregistrements synchronisés
Unexplained change|未解释的变动|未解釋的變動|Variation inexpliquée
Ending values|期末价值|期末價值|Valeurs finales
Source movements since checkpoint|检查点后的来源变动|檢查點後的來源變動|Mouvements sources depuis le point de contrôle
Journal / source|凭证 / 来源|憑證 / 來源|Écriture / source
Inventory change|库存变动|庫存變動|Variation des stocks
Sync status / IDs|同步状态 / ID|同步狀態 / ID|État de synchronisation / ID
New sales order|新建销售订单|新增銷售訂單|Nouvelle commande client
Search sales orders|搜索销售订单|搜尋銷售訂單|Rechercher les commandes clients
Search inventory|搜索库存|搜尋庫存|Rechercher les stocks
Search products|搜索产品|搜尋產品|Rechercher les produits
Balance|余额|餘額|Solde
Invoice|发票|發票|Facture
Bill|账单|帳單|Facture fournisseur
Credit|贷项|貸項|Crédit
New invoice|新建发票|新增發票|Nouvelle facture
New supplier bill|新建供应商账单|新增供應商帳單|Nouvelle facture fournisseur
Create invoice|创建发票|建立發票|Créer une facture
Create bill|创建账单|建立帳單|Créer une facture fournisseur
Record payment|记录付款|記錄付款|Enregistrer un paiement
Record refund|记录退款|記錄退款|Enregistrer un remboursement
Preview / PDF|预览 / PDF|預覽 / PDF|Aperçu / PDF
Source / party|来源 / 对方|來源 / 對方|Source / tiers
Document|单据|單據|Document
Issue document|开立单据|開立單據|Émettre le document
Draft documents|草稿单据|草稿單據|Documents brouillons
Open balance|未付余额|未付餘額|Solde ouvert
Date|日期|日期|Date
Tax code|税码|稅碼|Code de taxe
No tax|无税|無稅|Sans taxe
Total sales orders|销售订单总数|銷售訂單總數|Nombre total de commandes clients
Total Sales Orders|销售订单总数|銷售訂單總數|Nombre total de commandes clients
Ordered Products|订购产品数量|訂購產品數量|Produits commandés
Average Order Value|平均订单金额|平均訂單金額|Valeur moyenne des commandes
Average Order Margin|平均订单毛利率|平均訂單毛利率|Marge moyenne des commandes
Total Sales|销售总额|銷售總額|Ventes totales
Revenue By Period With Margin|期间收入与毛利|期間收入與毛利|Chiffre d’affaires et marge par période
Top Selling Products|畅销产品|暢銷產品|Produits les plus vendus
Sales by Product Tree|按产品类别销售|按產品類別銷售|Ventes par catégorie de produit
Sales dashboard|销售仪表板|銷售儀表板|Tableau de bord des ventes
Purchasing dashboard|采购仪表板|採購儀表板|Tableau de bord des achats
Inventory dashboard|库存仪表板|庫存儀表板|Tableau de bord des stocks
Revenue|收入|收入|Chiffre d’affaires
Margin|毛利|毛利|Marge
Date range|日期范围|日期範圍|Période
Previous date range|上一日期范围|上一日期範圍|Période précédente
This year|今年|今年|Cette année
Last year|去年|去年|Année précédente
This month|本月|本月|Ce mois
Last month|上月|上月|Mois précédent
Last 30 days|最近 30 天|最近 30 天|30 derniers jours
Last 90 days|最近 90 天|最近 90 天|90 derniers jours
Custom range|自定义范围|自訂範圍|Période personnalisée
From|从|從|Du
To|至|至|Au
Apply|应用|套用|Appliquer
Filters|筛选条件|篩選條件|Filtres
Export report CSV|导出报表 CSV|匯出報表 CSV|Exporter le rapport CSV
Warehouse report|仓库报表|倉庫報表|Rapport d’entrepôt
Generated|生成时间|產生時間|Généré
Report notes|报表说明|報表說明|Notes du rapport
Local warehouse report. Review history coverage before use.|本地仓库报表。使用前请检查历史记录覆盖范围。|本機倉庫報表。使用前請檢查歷史記錄涵蓋範圍。|Rapport d’entrepôt local. Vérifiez la couverture de l’historique avant utilisation.
Demand forecast|需求预测|需求預測|Prévision de la demande
Data mode|数据模式|資料模式|Mode de données
demo|示例|範例|démonstration
live|实际记录|實際記錄|données réelles
Assumptions|计划假设|計劃假設|Hypothèses
Description|产品说明|產品說明|Description
Recorded demand / data|记录需求 / 数据|記錄需求 / 資料|Demande enregistrée / données
Daily demand / next 30 days|每日需求 / 未来 30 天|每日需求 / 未來 30 天|Demande quotidienne / 30 prochains jours
Lead / safety / net stock / timely PO|交期 / 安全库存 / 净库存 / 按期采购|交期 / 安全庫存 / 淨庫存 / 按期採購|Délai / sécurité / stock net / achats à temps
Suggested purchase|建议采购|建議採購|Achat suggéré
selling days|销售日|銷售日|jours de vente
review before ordering|下单前请审核|下單前請審核|vérifier avant de commander
Enough for rolling-demand test|足够用于滚动需求测试|足夠用於滾動需求測試|Données suffisantes pour tester la demande glissante
No shipment history|没有发货历史|沒有出貨歷史|Aucun historique d’expédition
No recent demand|没有近期需求|沒有近期需求|Aucune demande récente
Limited history|历史记录不足|歷史記錄不足|Historique limité
Review data|检查数据|檢查資料|Vérifier les données
Stockout risk|缺货风险|缺貨風險|Risque de rupture
Replenish|补货|補貨|Réapprovisionner
Covered|已覆盖|已涵蓋|Couvert
Average daily shipped demand|平均每日发货需求|平均每日出貨需求|Demande quotidienne moyenne expédiée
Recent 30/30/30 days weighted 50/30/20%; includes zero-sale days|最近三个 30 天窗口，权重 50/30/20%；包括零销售日|最近三個 30 天視窗，權重 50/30/20%；包括零銷售日|Trois périodes de 30 jours pondérées 50/30/20 %; inclut les jours sans ventes
Planning estimate only. Demo data is synthetic. No supplier order or accounting export.|仅供计划参考。示例数据为模拟数据，不发送供应商订单或会计数据。|僅供計劃參考。範例資料為模擬資料，不傳送供應商訂單或會計資料。|Estimation de planification seulement. Les données de démonstration sont synthétiques. Aucune commande fournisseur ni export comptable.
No records yet.|暂无记录。|尚無記錄。|Aucun enregistrement pour le moment.
This record is unavailable|此记录不可用|此記錄無法使用|Ce dossier n’est pas disponible
Return to overview|返回概览|返回概覽|Retour à la vue d’ensemble
Loading inventory comparison…|正在加载库存对账…|正在載入庫存對帳…|Chargement du rapprochement des stocks…
Loading QuickBooks connection…|正在加载 QuickBooks 连接…|正在載入 QuickBooks 連線…|Chargement de la connexion QuickBooks…
Connect sandbox|连接沙盒|連接沙盒|Connecter le bac à sable
Disconnect|断开连接|中斷連線|Déconnecter
Refresh references|刷新关联资料|重新整理關聯資料|Actualiser les références
Prepare|准备|準備|Préparer
Send|发送|傳送|Envoyer
Retry|重试|重試|Réessayer
Reconcile balances|核对余额|核對餘額|Rapprocher les soldes
Use these records|使用这些记录|使用這些記錄|Utiliser ces enregistrements
Sign in|登录|登入|Se connecter
Sign out|退出登录|登出|Se déconnecter
Username|用户名|使用者名稱|Nom d’utilisateur
Password|密码|密碼|Mot de passe
Reset demo|重置示例|重設範例|Réinitialiser la démonstration
Download a backup|下载备份|下載備份|Télécharger une sauvegarde
Restore a backup|恢复备份|還原備份|Restaurer une sauvegarde
Prototype scope|原型范围|原型範圍|Portée du prototype
Chinese data & documents / 中文|中文数据与单据|中文資料與單據|Données et documents chinois
Documents / 文档|单据|單據|Documents
Product catalog CSV|产品目录 CSV|產品目錄 CSV|Catalogue de produits CSV
Save snapshot|保存快照|儲存快照|Enregistrer l’instantané
Save a labelled valuation snapshot|保存命名估值快照|儲存命名估值快照|Enregistrer un instantané de valorisation nommé
Snapshot label / 名称 / 名稱|快照名称|快照名稱|Nom de l’instantané
New zero-stock product|无库存的新产品|無庫存的新產品|Nouveau produit sans stock
Owned warehouse|自有仓库|自有倉庫|Entrepôt détenu
No preserved snapshot exists at or before this date/time.|在此日期 / 时间之前没有保存的快照。|在此日期 / 時間之前沒有保存的快照。|Aucun instantané conservé à cette date ou avant.
Choose a supported document language.|请选择支持的单据语言。|請選擇支援的單據語言。|Choisissez une langue de document prise en charge.
Review preserved stock values using the costs recorded at each snapshot.|使用各快照保存的成本查看历史库存价值。|使用各快照保存的成本檢視歷史庫存價值。|Consultez les valeurs conservées avec les coûts enregistrés dans chaque instantané.
Trace FIFO receipt layers, shipment consumption and restored customer-return values.|追踪 FIFO 收货层、发货消耗及客户退货恢复价值。|追蹤 FIFO 收貨層、出貨消耗及客戶退貨恢復價值。|Suivez les couches FIFO, leur consommation à l’expédition et les valeurs des retours clients.
Return quantities are checked against shipped or received quantities. Customer returns enter quality hold for inspection.|退货数量按已发货或已收货数量校验。客户退货进入质量冻结区进行检验。|退貨數量依已出貨或已收貨數量檢核。客戶退貨進入品質凍結區進行檢驗。|Les quantités retournées sont vérifiées par rapport aux quantités expédiées ou reçues. Les retours clients passent en contrôle qualité.
Checkpoint movement matched. The starting historical difference is retained.|检查点变动一致。保留期初历史差额。|檢查點變動一致。保留期初歷史差額。|La variation concorde. L’écart historique initial est conservé.
I reviewed the scope and preservation policy.|我已检查范围及保留记录规则。|我已檢查範圍及保留記錄規則。|J’ai vérifié la portée et les règles de conservation.
FIFO book value is the full remaining-layer sum, not next-unit cost multiplied by quantity. Captured unit cost is informational. Missing-cost rows are excluded from known value; sample opening costs stay labelled.|FIFO 账面价值是剩余成本层合计，不是下一件成本乘以数量。保存的单位成本仅供参考。缺失成本不计入已知价值；示例期初成本保留标记。|FIFO 帳面價值為剩餘成本層合計，並非下一件成本乘以數量。保存的單位成本僅供參考。缺失成本不計入已知價值；範例期初成本保留標記。|La valeur FIFO est la somme des couches restantes, et non le prochain coût multiplié par la quantité. Le coût enregistré est indicatif. Les coûts manquants sont exclus; les coûts initiaux de démonstration restent identifiés.
`;
export const catalogue=Object.fromEntries((rows.trim()+'\n'+extraRows.trim()+'\n'+unitRows.trim()+'\n'+salesRows.trim()+'\n'+crmRows.trim()+'\n'+productionRows.trim()).split('\n').map(line=>{const [key,sc,tc,fr,...extra]=line.split('|');if(!key||!sc||!tc||!fr||extra.length)throw Error('Invalid locale entry: '+line);return [key,{'zh-Hans':sc,'zh-Hant':tc,fr}];}));

catalogue['Create a new product with no stock before enabling FIFO.']={'zh-Hans':'启用 FIFO 前，请先创建没有库存的新产品。','zh-Hant':'啟用 FIFO 前，請先建立沒有庫存的新產品。',fr:'Créez un produit sans stock avant d’activer FIFO.'};

catalogue['Inventory records are saved in the shared workspace and included in backups.']={'zh-Hans':'库存记录保存在共享工作区，并包含在备份中。','zh-Hant':'庫存記錄儲存在共用工作區，並包含於備份中。',fr:'Les données de stock sont enregistrées dans l’espace partagé et incluses dans les sauvegardes.'};

catalogue['The save could not be confirmed. Refresh and check the record before trying again.']={'zh-Hans':'无法确认保存结果。请刷新并检查记录后再重试。','zh-Hant':'無法確認儲存結果。請重新整理並檢查記錄後再重試。',fr:'L’enregistrement n’a pas pu être confirmé. Actualisez et vérifiez la fiche avant de réessayer.'};

// Save recovery, access and staging guidance.
Object.assign(catalogue,{
 "Pending save recovery needs browser session storage. Enable it before saving.": {
  "zh-Hans": "保存恢复需要浏览器会话存储。请启用后再保存。",
  "zh-Hant": "儲存復原需要瀏覽器工作階段儲存空間。請啟用後再儲存。",
  "fr": "La reprise nécessite le stockage de session du navigateur. Activez-le avant d’enregistrer."
 },
 "An earlier save is unconfirmed. Open Data & settings and retry the pending save before entering another change.": {
  "zh-Hans": "先前的保存尚未确认。请打开数据与设置，重试待确认的保存，再输入其他更改。",
  "zh-Hant": "先前的儲存尚未確認。請開啟資料與設定，重試待確認的儲存，再輸入其他變更。",
  "fr": "Un enregistrement précédent reste à confirmer. Ouvrez Données et paramètres et réessayez-le avant une nouvelle modification."
 },
 "Unconfirmed save": {
  "zh-Hans": "未确认的保存",
  "zh-Hant": "未確認的儲存",
  "fr": "Enregistrement à confirmer"
 },
 "Retry pending save": {
  "zh-Hans": "重试待确认的保存",
  "zh-Hant": "重試待確認的儲存",
  "fr": "Réessayer l’enregistrement"
 },
 "Retry the original save. Its values and request identity are preserved; a confirmed save is not repeated.": {
  "zh-Hans": "重试原始保存。数值和请求标识保持不变；已确认的保存不会重复执行。",
  "zh-Hant": "重試原始儲存。數值與請求識別保持不變；已確認的儲存不會重複執行。",
  "fr": "Réessayez l’enregistrement initial. Ses valeurs et son identifiant sont conservés ; une opération confirmée ne sera pas répétée."
 },
 "Your Viewer account can browse records. Saving changes requires an authorized role.": {
  "zh-Hans": "访客账户可以浏览记录。保存更改需要具有授权的角色。",
  "zh-Hant": "檢視者帳戶可以瀏覽記錄。儲存變更需要具有授權的角色。",
  "fr": "Votre compte permet de consulter les données. Un rôle autorisé est requis pour enregistrer."
 },
 "Cloud mobile access": {
  "zh-Hans": "云端移动访问",
  "zh-Hant": "雲端行動存取",
  "fr": "Accès mobile au cloud"
 },
 "Warehouse scanning uses local Harbor in this phase. Cloud mobile saving is unavailable.": {
  "zh-Hans": "本阶段仓库扫描使用本地 Harbor。云端移动保存尚未开放。",
  "zh-Hant": "此階段倉庫掃描使用本地 Harbor。雲端行動儲存尚未開放。",
  "fr": "À cette étape, la lecture en entrepôt utilise Harbor local. L’enregistrement mobile cloud est indisponible."
 },
 "You can browse cloud inventory in the full Harbor app. Your account permissions still apply.": {
  "zh-Hans": "您可在完整 Harbor 应用中浏览云端库存。账户权限仍然适用。",
  "zh-Hant": "您可在完整 Harbor 應用程式中瀏覽雲端庫存。帳戶權限仍然適用。",
  "fr": "Consultez le stock cloud dans l’application Harbor complète. Les droits de votre compte restent applicables."
 },
 "Open Harbor inventory": {
  "zh-Hans": "打开 Harbor 库存",
  "zh-Hant": "開啟 Harbor 庫存",
  "fr": "Ouvrir le stock Harbor"
 },
 "Inventory editing is enabled for your role.": {
  "zh-Hans": "您的角色已获准编辑库存。",
  "zh-Hant": "您的角色已獲准編輯庫存。",
  "fr": "Votre rôle autorise la modification du stock."
 },
 "Inventory is read-only for your role.": {
  "zh-Hans": "您的角色只能查看库存。",
  "zh-Hant": "您的角色只能檢視庫存。",
  "fr": "Votre rôle permet de consulter le stock."
 },
 "Manufacturing actions follow your role permissions.": {
  "zh-Hans": "制造操作遵循您的角色权限。",
  "zh-Hant": "製造操作遵循您的角色權限。",
  "fr": "Les opérations de fabrication suivent les droits de votre rôle."
 },
 "Manufacturing is read-only for your role.": {
  "zh-Hans": "您的角色只能查看制造记录。",
  "zh-Hant": "您的角色只能檢視製造記錄。",
  "fr": "Votre rôle permet de consulter la fabrication."
 },
 "CRM editing is enabled for your role.": {
  "zh-Hans": "您的角色已获准编辑客户关系管理记录。",
  "zh-Hant": "您的角色已獲准編輯客戶關係管理記錄。",
  "fr": "Votre rôle autorise la modification du CRM."
 },
 "CRM is read-only for your role.": {
  "zh-Hans": "您的角色只能查看客户关系管理记录。",
  "zh-Hant": "您的角色只能檢視客戶關係管理記錄。",
  "fr": "Votre rôle permet de consulter le CRM."
 }
});

Object.assign(catalogue,{'Your role cannot perform this action.':{'zh-Hans':'您的角色不能执行此操作。','zh-Hant':'您的角色無法執行此操作。',fr:'Votre rôle ne permet pas cette action.'}});

Object.assign(catalogue,{
 'Loading server audit…':{'zh-Hans':'正在加载服务器审计记录…','zh-Hant':'正在載入伺服器稽核記錄…',fr:'Chargement du journal du serveur…'},
 'Server audit could not be loaded.':{'zh-Hans':'无法加载服务器审计记录。','zh-Hant':'無法載入伺服器稽核記錄。',fr:'Impossible de charger le journal du serveur.'},
 'Retry audit':{'zh-Hans':'重试加载审计记录','zh-Hant':'重試載入稽核記錄',fr:'Réessayer le journal'}
});

// Cloud sandbox connection and read-only comparisons.
Object.assign(catalogue,{
 "QuickBooks cloud sandbox": {
  "zh-Hans": "QuickBooks 云端沙盒",
  "zh-Hant": "QuickBooks 雲端沙盒",
  "fr": "Sandbox QuickBooks cloud"
 },
 "Connect a test company, load sandbox lists and compare inventory asset balances. Posting is disabled.": {
  "zh-Hans": "连接测试公司，加载沙盒列表并比较库存资产余额。已停用过账。",
  "zh-Hant": "連線測試公司、載入沙盒清單並比較庫存資產餘額。已停用過帳。",
  "fr": "Connectez une société de test, chargez les listes et comparez les soldes de stock. La comptabilisation est désactivée."
 },
 "Loading cloud sandbox connection…": {
  "zh-Hans": "正在加载云端沙盒连接…",
  "zh-Hant": "正在載入雲端沙盒連線…",
  "fr": "Chargement de la connexion sandbox cloud…"
 },
 "Posting disabled": {
  "zh-Hans": "已停用过账",
  "zh-Hant": "已停用過帳",
  "fr": "Comptabilisation désactivée"
 },
 "Sandbox not connected": {
  "zh-Hans": "尚未连接沙盒",
  "zh-Hant": "尚未連線沙盒",
  "fr": "Sandbox non connecté"
 },
 "Disconnect cloud sandbox": {
  "zh-Hans": "断开云端沙盒",
  "zh-Hant": "中斷雲端沙盒",
  "fr": "Déconnecter le sandbox cloud"
 },
 "Cloud sandbox setup steps": {
  "zh-Hans": "云端沙盒设置步骤",
  "zh-Hant": "雲端沙盒設定步驟",
  "fr": "Configuration du sandbox cloud"
 },
 "Create a separate Intuit Development app for cloud staging to keep the local PC connection separate.": {
  "zh-Hans": "为云端测试创建独立的 Intuit 开发应用，以保留本地电脑的独立连接。",
  "zh-Hant": "為雲端測試建立獨立的 Intuit 開發應用程式，以保留本機電腦的獨立連線。",
  "fr": "Créez une application Intuit Development distincte pour conserver la connexion locale séparément."
 },
 "Use QuickBooks Online Accounting access and a sandbox company.": {
  "zh-Hans": "使用 QuickBooks Online Accounting 权限及沙盒公司。",
  "zh-Hant": "使用 QuickBooks Online Accounting 權限及沙盒公司。",
  "fr": "Utilisez l’accès QuickBooks Online Accounting et une société sandbox."
 },
 "Register this exact Development redirect URI:": {
  "zh-Hans": "注册此完全一致的开发重定向地址：",
  "zh-Hant": "註冊此完全相同的開發重新導向網址：",
  "fr": "Enregistrez exactement cette URI de redirection Development :"
 },
 "Enter Development keys and the sandbox Company ID here, then select Connect sandbox.": {
  "zh-Hans": "在此输入开发密钥和沙盒公司编号，然后选择连接沙盒。",
  "zh-Hant": "在此輸入開發金鑰和沙盒公司編號，然後選擇連線沙盒。",
  "fr": "Saisissez les clés Development et l’identifiant de société, puis choisissez Connecter le sandbox."
 },
 "Client secrets and tokens are encrypted on the server. Do not paste them into chat.": {
  "zh-Hans": "客户端密钥和令牌在服务器上加密。请勿将其粘贴到聊天中。",
  "zh-Hant": "用戶端密鑰和權杖在伺服器上加密。請勿將其貼到聊天中。",
  "fr": "Les secrets et jetons sont chiffrés sur le serveur. Ne les collez pas dans le chat."
 },
 "Sandbox lists": {
  "zh-Hans": "沙盒列表",
  "zh-Hant": "沙盒清單",
  "fr": "Listes du sandbox"
 },
 "Lists loaded at": {
  "zh-Hans": "列表加载时间",
  "zh-Hant": "清單載入時間",
  "fr": "Listes chargées le"
 },
 "Inventory asset balance comparison": {
  "zh-Hans": "库存资产余额比较",
  "zh-Hant": "庫存資產餘額比較",
  "fr": "Comparaison des soldes de stock"
 },
 "Select only the sandbox accounts that represent Harbor inventory. Existing sandbox sample data can cause a difference.": {
  "zh-Hans": "仅选择代表 Harbor 库存的沙盒科目。现有沙盒示例数据可能导致差额。",
  "zh-Hant": "僅選擇代表 Harbor 庫存的沙盒科目。現有沙盒範例資料可能導致差額。",
  "fr": "Choisissez uniquement les comptes représentant le stock Harbor. Les exemples du sandbox peuvent créer un écart."
 },
 "Load sandbox lists to choose inventory asset accounts.": {
  "zh-Hans": "加载沙盒列表以选择库存资产科目。",
  "zh-Hant": "載入沙盒清單以選擇庫存資產科目。",
  "fr": "Chargez les listes pour choisir les comptes de stock."
 },
 "Compare balances": {
  "zh-Hans": "比较余额",
  "zh-Hant": "比較餘額",
  "fr": "Comparer les soldes"
 },
 "Harbor inventory value": {
  "zh-Hans": "Harbor 库存价值",
  "zh-Hant": "Harbor 庫存價值",
  "fr": "Valeur du stock Harbor"
 },
 "Selected QuickBooks balance": {
  "zh-Hans": "所选 QuickBooks 余额",
  "zh-Hant": "所選 QuickBooks 餘額",
  "fr": "Solde QuickBooks sélectionné"
 },
 "Harbor revision": {
  "zh-Hans": "Harbor 版本",
  "zh-Hant": "Harbor 版本",
  "fr": "Révision Harbor"
 },
 "Compared at": {
  "zh-Hans": "比较时间",
  "zh-Hant": "比較時間",
  "fr": "Comparé le"
 },
 "No inventory, cost or accounting balance was adjusted.": {
  "zh-Hans": "未调整任何库存、成本或会计余额。",
  "zh-Hant": "未調整任何庫存、成本或會計餘額。",
  "fr": "Aucun stock, coût ou solde comptable n’a été ajusté."
 },
 "Some Harbor stock has no known cost. Review the missing costs before interpreting the difference.": {
  "zh-Hans": "部分 Harbor 库存缺少已知成本。请先核查缺失成本，再分析差额。",
  "zh-Hant": "部分 Harbor 庫存缺少已知成本。請先核查缺失成本，再分析差額。",
  "fr": "Certains stocks Harbor n’ont pas de coût connu. Vérifiez les coûts manquants avant d’interpréter l’écart."
 },
 "Some Harbor values use demo sample costs.": {
  "zh-Hans": "部分 Harbor 价值使用示例成本。",
  "zh-Hant": "部分 Harbor 價值使用範例成本。",
  "fr": "Certaines valeurs Harbor utilisent des coûts de démonstration."
 },
 "QuickBooks did not provide a balance for every selected account.": {
  "zh-Hans": "QuickBooks 未提供所有所选科目的余额。",
  "zh-Hant": "QuickBooks 未提供所有所選科目的餘額。",
  "fr": "QuickBooks n’a pas fourni le solde de chaque compte sélectionné."
 },
 "Connection history": {
  "zh-Hans": "连接历史",
  "zh-Hant": "連線歷程",
  "fr": "Historique de connexion"
 },
 "Cloud sandbox development keys": {
  "zh-Hans": "云端沙盒开发密钥",
  "zh-Hant": "雲端沙盒開發金鑰",
  "fr": "Clés Development du sandbox cloud"
 },
 "Use a separate Development app for cloud staging. Keep the local PC connection separate.": {
  "zh-Hans": "云端测试请使用独立的开发应用。保留本地电脑的独立连接。",
  "zh-Hant": "雲端測試請使用獨立的開發應用程式。保留本機電腦的獨立連線。",
  "fr": "Utilisez une application Development distincte et conservez la connexion locale séparément."
 },
 "Development Client ID": {
  "zh-Hans": "开发客户端编号",
  "zh-Hant": "開發用戶端編號",
  "fr": "Client ID Development"
 },
 "Development Client Secret": {
  "zh-Hans": "开发客户端密钥",
  "zh-Hant": "開發用戶端密鑰",
  "fr": "Client Secret Development"
 },
 "Sandbox Company ID": {
  "zh-Hans": "沙盒公司编号",
  "zh-Hant": "沙盒公司編號",
  "fr": "Identifiant de société sandbox"
 },
 "Save development keys": {
  "zh-Hans": "保存开发密钥",
  "zh-Hant": "儲存開發金鑰",
  "fr": "Enregistrer les clés Development"
 },
 "Loading sandbox lists…": {
  "zh-Hans": "正在加载沙盒列表…",
  "zh-Hant": "正在載入沙盒清單…",
  "fr": "Chargement des listes du sandbox…"
 },
 "Disconnect this cloud sandbox connection. The local PC connection and Harbor records are preserved.": {
  "zh-Hans": "断开此云端沙盒连接。本地电脑连接和 Harbor 记录将保留。",
  "zh-Hant": "中斷此雲端沙盒連線。本機電腦連線和 Harbor 記錄將保留。",
  "fr": "Déconnectez ce sandbox cloud. La connexion locale et les données Harbor sont conservées."
 },
 "Private accounting access is required.": {
  "zh-Hans": "需要私有会计访问权限。",
  "zh-Hant": "需要私人會計存取權限。",
  "fr": "Un accès comptable privé est requis."
 },
 "Cloud QuickBooks encryption is not configured.": {
  "zh-Hans": "尚未配置云端 QuickBooks 加密。",
  "zh-Hant": "尚未設定雲端 QuickBooks 加密。",
  "fr": "Le chiffrement QuickBooks cloud n’est pas configuré."
 },
 "Cloud QuickBooks credentials could not be opened. Contact the administrator.": {
  "zh-Hans": "无法解密云端 QuickBooks 凭据。请联系管理员。",
  "zh-Hant": "無法解密雲端 QuickBooks 憑證。請聯絡管理員。",
  "fr": "Impossible de déchiffrer les identifiants QuickBooks cloud. Contactez l’administrateur."
 },
 "QuickBooks could not be reached. No accounting record was sent.": {
  "zh-Hans": "无法连接 QuickBooks。未发送任何会计记录。",
  "zh-Hant": "無法連線 QuickBooks。未傳送任何會計記錄。",
  "fr": "QuickBooks est inaccessible. Aucune écriture comptable n’a été envoyée."
 },
 "QuickBooks returned an unreadable response. Try loading again.": {
  "zh-Hans": "QuickBooks 返回了无法读取的响应。请重试加载。",
  "zh-Hant": "QuickBooks 傳回無法讀取的回應。請重試載入。",
  "fr": "Réponse QuickBooks illisible. Réessayez le chargement."
 },
 "QuickBooks authorization needs reconnecting.": {
  "zh-Hans": "QuickBooks 授权需要重新连接。",
  "zh-Hant": "QuickBooks 授權需要重新連線。",
  "fr": "Reconnectez l’autorisation QuickBooks."
 },
 "QuickBooks is busy. Wait before loading again.": {
  "zh-Hans": "QuickBooks 繁忙。请稍候再加载。",
  "zh-Hant": "QuickBooks 忙碌中。請稍候再載入。",
  "fr": "QuickBooks est occupé. Patientez avant de recharger."
 },
 "QuickBooks rejected the connection or read request.": {
  "zh-Hans": "QuickBooks 拒绝了连接或读取请求。",
  "zh-Hant": "QuickBooks 拒絕連線或讀取請求。",
  "fr": "QuickBooks a refusé la connexion ou la lecture."
 },
 "QuickBooks returned incomplete authorization tokens.": {
  "zh-Hans": "QuickBooks 返回了不完整的授权令牌。",
  "zh-Hant": "QuickBooks 傳回不完整的授權權杖。",
  "fr": "QuickBooks a renvoyé des jetons incomplets."
 },
 "The sandbox company could not be verified.": {
  "zh-Hans": "无法验证沙盒公司。",
  "zh-Hant": "無法驗證沙盒公司。",
  "fr": "Impossible de vérifier la société sandbox."
 },
 "QuickBooks returned an invalid list.": {
  "zh-Hans": "QuickBooks 返回了无效列表。",
  "zh-Hant": "QuickBooks 傳回無效清單。",
  "fr": "QuickBooks a renvoyé une liste invalide."
 },
 "The sandbox list is too large for this staging connection.": {
  "zh-Hans": "沙盒列表超出此测试连接的大小限制。",
  "zh-Hant": "沙盒清單超出此測試連線的大小限制。",
  "fr": "La liste dépasse la capacité de cette connexion de test."
 },
 "Posting is disabled in this cloud phase.": {
  "zh-Hans": "此云端阶段已停用过账。",
  "zh-Hant": "此雲端階段已停用過帳。",
  "fr": "La comptabilisation est désactivée à cette étape cloud."
 },
 "Only the administrator can configure this connection.": {
  "zh-Hans": "仅管理员可以配置此连接。",
  "zh-Hant": "僅管理員可以設定此連線。",
  "fr": "Seul l’administrateur peut configurer cette connexion."
 },
 "QuickBooks settings changed. Refresh and review before retrying.": {
  "zh-Hans": "QuickBooks 设置已更改。请刷新并核查后重试。",
  "zh-Hant": "QuickBooks 設定已變更。請重新整理並核查後重試。",
  "fr": "Les paramètres QuickBooks ont changé. Actualisez et vérifiez avant de réessayer."
 },
 "Enter Development keys and the sandbox Company ID.": {
  "zh-Hans": "请输入开发密钥和沙盒公司编号。",
  "zh-Hant": "請輸入開發金鑰和沙盒公司編號。",
  "fr": "Saisissez les clés Development et l’identifiant de société sandbox."
 },
 "Enter a valid Development Client Secret.": {
  "zh-Hans": "请输入有效的开发客户端密钥。",
  "zh-Hant": "請輸入有效的開發用戶端密鑰。",
  "fr": "Saisissez un Client Secret Development valide."
 },
 "Development keys saved. Connect the sandbox next.": {
  "zh-Hans": "开发密钥已保存。接下来请连接沙盒。",
  "zh-Hant": "開發金鑰已儲存。接下來請連線沙盒。",
  "fr": "Clés Development enregistrées. Connectez ensuite le sandbox."
 },
 "Cloud sandbox disconnected.": {
  "zh-Hans": "云端沙盒已断开。",
  "zh-Hant": "雲端沙盒已中斷。",
  "fr": "Sandbox cloud déconnecté."
 },
 "Cloud tokens removed. Remove this app in Intuit if revocation was not confirmed.": {
  "zh-Hans": "云端令牌已移除。如未确认撤销，请在 Intuit 中移除此应用。",
  "zh-Hant": "雲端權杖已移除。如未確認撤銷，請在 Intuit 中移除此應用程式。",
  "fr": "Jetons cloud supprimés. Retirez l’application dans Intuit si la révocation n’est pas confirmée."
 },
 "Sandbox lists loaded. Posting remains disabled.": {
  "zh-Hans": "沙盒列表已加载。过账仍停用。",
  "zh-Hant": "沙盒清單已載入。過帳仍停用。",
  "fr": "Listes chargées. La comptabilisation reste désactivée."
 },
 "The sandbox and Harbor home currencies must match.": {
  "zh-Hans": "沙盒与 Harbor 的本位币必须相同。",
  "zh-Hant": "沙盒與 Harbor 的本位幣必須相同。",
  "fr": "Les devises de base du sandbox et de Harbor doivent correspondre."
 },
 "Choose inventory asset accounts for comparison.": {
  "zh-Hans": "请选择要比较的库存资产科目。",
  "zh-Hant": "請選擇要比較的庫存資產科目。",
  "fr": "Choisissez les comptes de stock à comparer."
 },
 "Choose active inventory asset accounts in the home currency.": {
  "zh-Hans": "请选择本位币下的有效库存资产科目。",
  "zh-Hant": "請選擇本位幣下的有效庫存資產科目。",
  "fr": "Choisissez des comptes de stock actifs dans la devise de base."
 },
 "Comparison saved. No balance or cost was changed.": {
  "zh-Hans": "比较已保存。未更改余额或成本。",
  "zh-Hant": "比較已儲存。未變更餘額或成本。",
  "fr": "Comparaison enregistrée. Aucun solde ni coût n’a changé."
 },
 "Authorization expired. Start Connect sandbox again.": {
  "zh-Hans": "授权已过期。请重新选择连接沙盒。",
  "zh-Hant": "授權已過期。請重新選擇連線沙盒。",
  "fr": "Autorisation expirée. Relancez Connecter le sandbox."
 },
 "Sandbox authorization was cancelled. You can connect again.": {
  "zh-Hans": "沙盒授权已取消。您可以重新连接。",
  "zh-Hant": "沙盒授權已取消。您可以重新連線。",
  "fr": "Autorisation annulée. Vous pouvez reconnecter le sandbox."
 },
 "The selected company does not match the sandbox Company ID.": {
  "zh-Hans": "所选公司与沙盒公司编号不匹配。",
  "zh-Hant": "所選公司與沙盒公司編號不符。",
  "fr": "La société choisie ne correspond pas à l’identifiant sandbox."
 },
 "QuickBooks did not return an authorization code.": {
  "zh-Hans": "QuickBooks 未返回授权码。",
  "zh-Hant": "QuickBooks 未傳回授權碼。",
  "fr": "QuickBooks n’a pas renvoyé de code d’autorisation."
 },
 "Cloud sandbox connected. Load sandbox lists next.": {
  "zh-Hans": "云端沙盒已连接。接下来请加载沙盒列表。",
  "zh-Hant": "雲端沙盒已連線。接下來請載入沙盒清單。",
  "fr": "Sandbox cloud connecté. Chargez ensuite les listes."
 },
 "The sandbox connection could not be verified. Check Development keys, Company ID and redirect URI, then connect again.": {
  "zh-Hans": "无法验证沙盒连接。请核查开发密钥、公司编号和重定向地址，然后重新连接。",
  "zh-Hant": "無法驗證沙盒連線。請核查開發金鑰、公司編號和重新導向網址，然後重新連線。",
  "fr": "Connexion sandbox non vérifiée. Vérifiez les clés Development, l’identifiant et l’URI, puis reconnectez-vous."
 },
 "Configured cloud sandbox": {
  "zh-Hans": "已配置云端沙盒",
  "zh-Hant": "已設定雲端沙盒",
  "fr": "Sandbox cloud configuré"
 },
 "Disconnected cloud sandbox": {
  "zh-Hans": "已断开云端沙盒",
  "zh-Hant": "已中斷雲端沙盒",
  "fr": "Sandbox cloud déconnecté"
 },
 "Loaded sandbox lists": {
  "zh-Hans": "已加载沙盒列表",
  "zh-Hant": "已載入沙盒清單",
  "fr": "Listes sandbox chargées"
 },
 "Compared inventory asset balances": {
  "zh-Hans": "已比较库存资产余额",
  "zh-Hant": "已比較庫存資產餘額",
  "fr": "Soldes de stock comparés"
 },
 "Connected cloud sandbox": {
  "zh-Hans": "已连接云端沙盒",
  "zh-Hant": "已連線雲端沙盒",
  "fr": "Sandbox cloud connecté"
 },
 "TaxCode": {
  "zh-Hans": "税码",
  "zh-Hant": "稅碼",
  "fr": "Code fiscal"
 },
 "QuickBooks is not connected in this demo.": {
  "zh-Hans": "此演示未连接 QuickBooks。",
  "zh-Hant": "此示範未連線 QuickBooks。",
  "fr": "QuickBooks n’est pas connecté dans cette démonstration."
 },
 "SANDBOX ONLY": {
  "zh-Hans": "仅限沙盒",
  "zh-Hant": "僅限沙盒",
  "fr": "SANDBOX UNIQUEMENT"
 },
 "Sandbox connected": {
  "zh-Hans": "沙盒已连接",
  "zh-Hant": "沙盒已連線",
  "fr": "Sandbox connecté"
 },
 "Account": {
  "zh-Hans": "科目",
  "zh-Hant": "科目",
  "fr": "Compte"
 },
 "Vendor": {
  "zh-Hans": "供应商",
  "zh-Hant": "供應商",
  "fr": "Fournisseur"
 },
 "TaxRate": {
  "zh-Hans": "税率",
  "zh-Hant": "稅率",
  "fr": "Taux de taxe"
 },
 "Translated labels are for display only. Original QuickBooks names and account IDs are preserved.": {
  "zh-Hans": "翻译标签仅用于显示。原始 QuickBooks 名称及科目编号保持不变。",
  "zh-Hant": "翻譯標籤僅用於顯示。原始 QuickBooks 名稱及科目編號保持不變。",
  "fr": "Les traductions servent uniquement à l’affichage. Les noms QuickBooks et identifiants de compte d’origine sont conservés."
 }
});

Object.assign(catalogue,receivingCatalogue);
for(const [key,value] of Object.entries(workflowCatalogue))if(!catalogue[key])catalogue[key]=value;
for(const [key,value] of Object.entries(securityCatalogue))if(!catalogue[key])catalogue[key]=value;

