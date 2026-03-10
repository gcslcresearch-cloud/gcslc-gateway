# Map of Authority — True Map of Nigeria (36 State Borders)

For **geographically accurate** Nigeria state borders in the GCSLC Sovereign Command dashboard:

- **Option A:** Place a state-level GeoJSON file here as `ng_state.geojson`. Each feature must have a state name in `properties` (e.g. `adm1_name`, `shapeName`, `name_1`, or `NAME_1`). The app uses the **geojson** library when available to validate. **13 coal-reserve states** (Enugu, Kogi, Benue, Nasarawa, Gombe, Adamawa, Delta, Edo, Ondo, Bauchi, Anambra, Ebonyi, Abia) are colored **Burnished Gold**; the other 23 states and FCT are **Sovereign Navy**.

- **Option B:** If this file is not present, the app will attempt to fetch and merge Nigeria administrative boundaries from HDX (requires network and `shapely`).

No generic octagon or placeholder shapes are used when real GeoJSON is available. This is the presidential directive: the map must be geographically accurate and high-prestige.
