# AWC Generative Eagle Engine (D7 Re-engineered)

React Three Fiber components for the GCSLC **Generative Eagle**: apex predator (sniffing / striking) and optional swarm.

## Dependencies

```bash
npm install three @react-three/fiber @react-three/drei
# or
pnpm add three @react-three/fiber @react-three/drei
```

## Usage

```jsx
import { AWCGenerativeEagleEngine } from './AWCGenerativeEagleEngine';

// Single eagle (placeholder mesh if no GLTF)
<AWCGenerativeEagleEngine isStriking={false} useGltf={false} />

// With golden_eagle.gltf in public/
<AWCGenerativeEagleEngine isStriking={false} gltfUrl="/golden_eagle.gltf" />

// Eagle + swarm (Samsung Good Lock–style)
<AWCGenerativeEagleEngine showSwarm swarmCount={50} useGltf={false} />
```

## Props

| Prop         | Type    | Default               | Description                                      |
|-------------|--------|------------------------|--------------------------------------------------|
| `isStriking`| bool   | `false`                | When true, disables sniffing hover animation.    |
| `showSwarm` | bool   | `false`                | Renders mini-eagle instances.                    |
| `swarmCount`| number | `50`                   | Number of swarm instances.                      |
| `gltfUrl`   | string | `'/golden_eagle.gltf'`| Path to eagle GLTF (used if `useGltf` is true). |
| `useGltf`   | bool   | `true`                 | Use GLTF model; if false, uses gold cone mesh.  |

## Exports

- **AWCGenerativeEagleEngine** — Full canvas + eagle (+ optional swarm).
- **ApexPredator** — Single eagle with `position`, `isStriking`, optional `scene`.
- **EagleSwarm** — Instanced placeholder swarm; `count` prop.

## Logic

- **Sniffing:** When `isStriking` is false, the eagle rotates on Y and bobs on Y each frame.
- **Float:** Wraps the eagle in `<Float>` for gentle hover (drei).
- **Swarm:** Uses `<Instances>` / `<Instance>` for many small cones (replace geometry with eagle mesh if desired).

Place `golden_eagle.gltf` in your app’s `public/` (or set `gltfUrl`) to use a real model; otherwise set `useGltf={false}` for the built-in placeholder.
