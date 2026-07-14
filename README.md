# Wayland Arc

Wayland Arc is an ongoing project to build an industrial dashboard and computer vision pipeline for real-time manufacturing analysis. The goal is to bridge the gap between shop-floor hardware and clean, insightful analytics.

Following my recent shift to Welding Engineering from Computer Science, I wanted to create a project that bridges my background in software development with the additive manufacturing research I am currently conducting. What started as an elementary exercise in data processing has evolved into a project I am committed to seeing through, bridging the gap between shop-floor hardware and modern software analytics.

## How the System Works

At a high level, the system functions as a continuous feedback loop. It initializes by establishing a central control hub that simultaneously launches a live user dashboard and a series of background processing tasks. These background tasks handle the heavy lifting: ingesting raw visual and motion data from the manufacturing environment, running it through an analytics engine to derive actionable performance insights, and managing that data in a persistent store so the dashboard remains up-to-the-minute. Throughout this cycle, an automated monitoring layer keeps watch, immediately signaling alerts if the process parameters drift outside of acceptable tolerances.

## Where We Are Now: Software First

Building hardware-integrated systems takes capital. Since the project is currently bootstrapping, Wayland Arc is operating in a "software-first" simulation phase. I am stress-testing the entire architecture by subjecting the data pipelines to synthetic, high-volume sensor telemetry and pre-recorded high-resolution video datasets. This allows me to measure system latency, throughput, and bottleneck points under peak load conditions, ensuring the software foundation will be bulletproof and ready to scale once physical sensors are integrated.

## The Roadmap: Moving to the Factory Floor

Once funding allows for physical hardware, the goal is to deploy Wayland Arc into live manufacturing environments:

1.  **Eyes on the Line:** Integrating high-speed cameras to monitor advanced processes like robotic Gas Metal Arc Pulsed welding and Directed Energy Deposition (DED).
2.  **Live Defect Catching:** Transitioning from simulated streams to real-time feeds to catch issues like porosity and spatter instantly.
3.  **PLC Handshakes:** Interfacing directly with factory machinery to sync visual data with robot kinematics and machine states.
4.  **Real-Time Shop Dashboards:** Streaming synchronized data to provide operators with immediate process health insights.
5.  **Automated Quality Control:** Triggering real-time notifications the moment parameters drift out of spec.

Thank you! Be kind :D
