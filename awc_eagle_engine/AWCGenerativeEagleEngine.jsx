// AWC Generative Eagle Engine (D7 Re-engineered) — Apex Engine v4.0
// Galadiman Ruwa Center (GCSLC) — 8R Stealth Paradigm | Sovereign UI Manifesto
// Use with: @react-three/fiber, @react-three/drei, three, framer-motion

import { useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useGLTF, Float, Instances, Instance } from '@react-three/drei';
import { motion } from 'framer-motion';

function ApexPredator({ position = [0, 0, 0], isStriking = false, scene = null }) {
  const eagleRef = useRef(null);

  useFrame((state) => {
    if (!eagleRef.current) return;
    // Generative 'Sniffing' Logic — hover when not striking
    if (!isStriking) {
      eagleRef.current.rotation.y = Math.sin(state.clock.elapsedTime) * 0.2;
      eagleRef.current.position.y += Math.cos(state.clock.elapsedTime) * 0.01;
    }
  });

  const content = scene ? (
    <primitive
      ref={eagleRef}
      object={scene.clone()}
      scale={1.5}
      position={position}
    />
  ) : (
    <mesh ref={eagleRef} position={position} scale={[1.5, 1, 1.5]}>
      <coneGeometry args={[0.3, 0.6, 4]} />
      <meshStandardMaterial color="#FFD700" metalness={0.6} roughness={0.3} />
    </mesh>
  );

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
      {content}
    </Float>
  );
}

function EagleWithModel({ position, isStriking, url }) {
  const { scene } = useGLTF(url || '/golden_eagle.gltf');
  return <ApexPredator position={position} isStriking={isStriking} scene={scene} />;
}

// Swarm Logic inspired by Samsung Good Lock customization
function EagleSwarm({ count = 50 }) {
  return (
    <Instances limit={count} range={count}>
      <coneGeometry args={[0.1, 0.3, 3]} />
      <meshStandardMaterial color="#FFD700" metalness={0.5} roughness={0.4} />
      {Array.from({ length: count }).map((_, i) => (
        <Instance
          key={i}
          position={[Math.random() * 10 - 5, 2 + Math.random() * 6, Math.random() * 10 - 5]}
        />
      ))}
    </Instances>
  );
}

// Sovereign UI: framer-motion container for strike/reveal transitions
const SovereignCanvasWrapper = motion.div;

export function AWCGenerativeEagleEngine({
  isStriking = false,
  showSwarm = false,
  swarmCount = 50,
  gltfUrl = '/golden_eagle.gltf',
  useGltf = true,
}) {
  return (
    <SovereignCanvasWrapper
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      style={{ width: '100%', height: '100%', minHeight: 320 }}
    >
      <Canvas camera={{ position: [0, 5, 10], fov: 50 }} dpr={[1, 2]}>
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <pointLight position={[-5, 5, 5]} color="#FFD700" intensity={0.5} />
        <Suspense fallback={null}>
          {useGltf ? (
            <EagleWithModel position={[0, 2, 0]} isStriking={isStriking} url={gltfUrl} />
          ) : (
            <ApexPredator position={[0, 2, 0]} isStriking={isStriking} />
          )}
          {showSwarm && <EagleSwarm count={swarmCount} />}
        </Suspense>
      </Canvas>
    </SovereignCanvasWrapper>
  );
}

export { ApexPredator, EagleSwarm };
