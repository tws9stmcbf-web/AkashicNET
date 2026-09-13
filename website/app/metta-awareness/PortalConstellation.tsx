"use client";

import { PointerEvent, WheelEvent, useRef, useState } from "react";
import styles from "./metta-awareness.module.css";

const portals = [
  { level:"01", title:"Arrive", note:"Pause and notice", href:"#practice", className:"portalOne" },
  { level:"02", title:"Relate", note:"Four capacities", href:"#capacities", className:"portalTwo" },
  { level:"03", title:"Inquire", note:"13 revisable lenses", href:"#thirteen", className:"portalThree" },
  { level:"04", title:"Listen", note:"Guided media", href:"#listen", className:"portalFour" },
  { level:"05", title:"Contemplate", note:"Sound, symbol, unknown", href:"#cymatics", className:"portalFive" },
];

export default function PortalConstellation() {
  const fieldRef = useRef<HTMLElement>(null);
  const dragRef = useRef({active:false,x:0,y:0,rx:0,ry:0});
  const [view,setView] = useState({rx:-4,ry:7,zoom:1});

  function applyPointer(x:number,y:number){
    const rect=fieldRef.current?.getBoundingClientRect();
    if(!rect) return;
    const nx=((x-rect.left)/rect.width-.5)*2;
    const ny=((y-rect.top)/rect.height-.5)*2;
    setView(v=>({...v,rx:-ny*7,ry:nx*10}));
  }

  function onPointerDown(event:PointerEvent<HTMLElement>){
    dragRef.current={active:true,x:event.clientX,y:event.clientY,rx:view.rx,ry:view.ry};
    event.currentTarget.setPointerCapture(event.pointerId);
  }

  function onPointerMove(event:PointerEvent<HTMLElement>){
    const drag=dragRef.current;
    if(drag.active){
      setView(v=>({...v,rx:Math.max(-16,Math.min(16,drag.rx-(event.clientY-drag.y)*.08)),ry:Math.max(-20,Math.min(20,drag.ry+(event.clientX-drag.x)*.1))}));
    }else if(event.pointerType==="mouse"){
      applyPointer(event.clientX,event.clientY);
    }
  }

  function stopDrag(){dragRef.current.active=false}

  function onWheel(event:WheelEvent<HTMLElement>){
    if(Math.abs(event.deltaY)<2) return;
    setView(v=>({...v,zoom:Math.max(.88,Math.min(1.12,v.zoom-event.deltaY*.00035))}));
  }

  function resetView(){setView({rx:-4,ry:7,zoom:1})}

  return (
    <section
      ref={fieldRef}
      className={styles.portalMap}
      aria-labelledby="portal-map-title"
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={stopDrag}
      onPointerCancel={stopDrag}
      onPointerLeave={stopDrag}
      onWheel={onWheel}
    >
      <div className={styles.portalIntro}>
        <p className={styles.label}>Spatial portal constellation</p>
        <h2 id="portal-map-title">Choose your depth.</h2>
        <p>Begin anywhere. Move inward when the language, context and uncertainty boundaries feel clear. “Deeper” describes the level of inquiry, never the value or awareness of a person.</p>
        <div className={styles.spatialInstructions} id="portal-instructions">
          <span>Drag or move to explore</span>
          <span>Scroll to adjust depth</span>
          <span>Tap a portal to enter</span>
        </div>
        <button type="button" onClick={resetView} className={styles.resetView}>Reset spatial view</button>
      </div>
      <nav
        className={styles.spatialStage}
        aria-label="Mettā-Awareness depth map"
        aria-describedby="portal-instructions"
        style={{"--rx":`${view.rx}deg`,"--ry":`${view.ry}deg`,"--zoom":view.zoom} as React.CSSProperties}
      >
        <div className={styles.portals}>
          <i className={styles.depthPlaneOne} aria-hidden="true"/>
          <i className={styles.depthPlaneTwo} aria-hidden="true"/>
          {portals.map(portal=>
            <a key={portal.level} className={styles[portal.className]} href={portal.href}>
              <span>{portal.level}</span><strong>{portal.title}</strong><small>{portal.note}</small>
            </a>
          )}
        </div>
      </nav>
    </section>
  );
}
