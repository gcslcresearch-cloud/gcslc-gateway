# Map of Authority — Nigeria GeoJSON

For **real Nigeria state borders** in the GCSLC Sovereign Command dashboard:

- **Option A:** Place a state-level GeoJSON file here as `ng_state.geojson`. Each feature must have `properties.adm1_name` equal to the state name (e.g. `"Kogi"`, `"Enugu"`). 13 coal-rich states will be colored Gold (#FFD700), others Navy (#000080).

- **Option B:** If this file is not present, the app will attempt to fetch and merge the Nigeria administrative boundaries GeoJSON from HDX (requires network and `shapely`).

No yellow octagon or placeholder shapes are used when real GeoJSON is available.
