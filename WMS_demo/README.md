# Chmltech WMS browser demo

Serve this folder at `/WMS_demo/` on any static host. Open `index.html` through HTTP/HTTPS, rather than file://. No Node server, database, login, cloud credentials or package installation is required on the host.

Records are fictional and stored under `chmltech:WMS_demo:warehouse:v1` in this browser. Reset changes only that warehouse key. Clearing browser data removes the saved warehouse. Browser tabs share the local demo; devices and browser profiles do not sync. Do not enter real customer data.

The full browser interface includes English sample products and editable Each, Pack of 3, Carton of 12 and Pallet of 480 conversions. External integrations and real user administration remain disconnected. PDF vendor libraries, fonts and their licenses are included.

Source: https://github.com/quakfoolee-dotcom/harbor-wms — demo/browser-*.mjs, scripts/build-browser-demo.mjs and scripts/browser-demo-patches.mjs (public-demo fonts, wording, controls and translations). After copying a build to the website, run its content/gen/seo_pass.py to add analytics. Rebuild from source to update the generated files.
