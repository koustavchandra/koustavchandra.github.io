---
layout: default
---

<!-- Section -->
<section>
    <header class="major">
        <h2>News 🗞️</h2>
    </header>
    
    <div class="timeline">
        <article class="timeline-item">
            <span class="icon fa-globe"></span>
            <div class="content">
                <h3>Oct 2025</h3>
                <p><strong>AEI Potsdam! 🥨</strong> Switched to AEI jersey. German chapter begins!</p>
            </div>
        </article>
                
        <article class="timeline-item">
            <span class="icon fa-trophy"></span>
            <div class="content">
                <h3>Aug 2024</h3>
                <p><strong>Thesis award! 🏆</strong> Naik & Rastogi Award for my PhD work. Sleep deprivation paid off! 😁</p>
            </div>
        </article>
        
        <article class="timeline-item">
            <span class="icon fa-users"></span>
            <div class="content">
                <h3>Oct 2023</h3>
                <p><strong>Penn State! 🦁</strong> Officially a Nittany Lion at IGC.</p>
            </div>
        </article>
        
        <article class="timeline-item">
            <span class="icon fa-graduation-cap"></span>
            <div class="content">
                <h3>Sep 2023</h3>
                <p><strong>PhD done! 🎓</strong> Thesis defeated. Coffee consumed. Dr. Chandra activated! ☕</p>
            </div>
        </article>
    </div>
</section>

<style>
.timeline {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.timeline-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    border-left: 4px solid #4CAF50;
}

.timeline-item .icon {
    flex-shrink: 0;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #4CAF50;
    color: white;
    border-radius: 50%;
    font-size: 0.9rem;
}

.timeline-item .content {
    flex: 1;
}

.timeline-item h3 {
    margin: 0 0 0.5rem 0;
    color: #4CAF50;
    font-weight: bold;
}

.timeline-item p {
    margin: 0;
    line-height: 1.6;
}

@media (max-width: 768px) {
    .timeline-item {
        padding: 1rem;
        gap: 0.75rem;
    }
    
    .timeline-item .icon {
        width: 1.5rem;
        height: 1.5rem;
        font-size: 0.8rem;
    }
}
</style>