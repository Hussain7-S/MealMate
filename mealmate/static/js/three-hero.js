/*
  MealMate hero scene.
  A dark charcoal void with a rotating "thali" (plate) made of a torus rim
  and a few glowing food orbs orbiting it, plus soft rising steam particles.
  This is the page's signature visual: it literally re-stages the brief's
  own story — a hot plate of food, waiting, on a quiet rainy evening.
*/
(function () {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
  camera.position.set(0, 1.4, 7);

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  function resize() {
    const { clientWidth: w, clientHeight: h } = canvas;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  // Lighting: warm key light (turmeric) + cool rim (plum) for food-photography feel
  scene.add(new THREE.AmbientLight(0x2a211b, 1.2));
  const key = new THREE.PointLight(0xE8A93A, 3.5, 20);
  key.position.set(3, 4, 4);
  scene.add(key);
  const rim = new THREE.PointLight(0x4A2545, 3, 20);
  rim.position.set(-4, -2, -3);
  scene.add(rim);

  // The plate: a torus rim + inner disc
  const plateGroup = new THREE.Group();
  const rimGeo = new THREE.TorusGeometry(2.1, 0.14, 24, 100);
  const rimMat = new THREE.MeshStandardMaterial({ color: 0xFBF3E7, metalness: 0.3, roughness: 0.4 });
  const rimMesh = new THREE.Mesh(rimGeo, rimMat);
  rimMesh.rotation.x = Math.PI / 2;
  plateGroup.add(rimMesh);

  const discGeo = new THREE.CircleGeometry(1.9, 64);
  const discMat = new THREE.MeshStandardMaterial({ color: 0x1C1410, metalness: 0.1, roughness: 0.8 });
  const disc = new THREE.Mesh(discGeo, discMat);
  disc.rotation.x = -Math.PI / 2;
  disc.position.y = -0.02;
  plateGroup.add(disc);

  // Food orbs: chili-red, turmeric, basil-green spheres arranged like curry bowls
  const foodColors = [0xE8492E, 0xE8A93A, 0x3F6B4A, 0xE8492E];
  const foodOrbs = [];
  foodColors.forEach((color, i) => {
    const geo = new THREE.SphereGeometry(0.34 + (i % 2) * 0.08, 32, 32);
    const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.35, metalness: 0.15, emissive: color, emissiveIntensity: 0.12 });
    const orb = new THREE.Mesh(geo, mat);
    const angle = (i / foodColors.length) * Math.PI * 2;
    orb.position.set(Math.cos(angle) * 1.15, 0.22, Math.sin(angle) * 1.15);
    plateGroup.add(orb);
    foodOrbs.push(orb);
  });

  plateGroup.rotation.x = 0.5;
  plateGroup.position.y = -0.4;
  scene.add(plateGroup);

  // Steam: small rising particles
  const steamCount = 60;
  const steamGeo = new THREE.BufferGeometry();
  const positions = new Float32Array(steamCount * 3);
  const speeds = new Float32Array(steamCount);
  for (let i = 0; i < steamCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 2.2;
    positions[i * 3 + 1] = Math.random() * 2 - 0.5;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 2.2;
    speeds[i] = 0.004 + Math.random() * 0.006;
  }
  steamGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const steamMat = new THREE.PointsMaterial({ color: 0xFBF3E7, size: 0.05, transparent: true, opacity: 0.35 });
  const steam = new THREE.Points(steamGeo, steamMat);
  scene.add(steam);

  let raf;
  function animate() {
    raf = requestAnimationFrame(animate);
    plateGroup.rotation.y += 0.0035;
    foodOrbs.forEach((orb, i) => {
      orb.position.y = 0.22 + Math.sin(Date.now() * 0.001 + i) * 0.05;
    });

    const pos = steamGeo.attributes.position.array;
    for (let i = 0; i < steamCount; i++) {
      pos[i * 3 + 1] += speeds[i];
      if (pos[i * 3 + 1] > 2.2) pos[i * 3 + 1] = -0.5;
    }
    steamGeo.attributes.position.needsUpdate = true;

    renderer.render(scene, camera);
  }

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  resize();
  window.addEventListener('resize', resize);
  if (!prefersReducedMotion) {
    animate();
  } else {
    renderer.render(scene, camera);
  }
})();
