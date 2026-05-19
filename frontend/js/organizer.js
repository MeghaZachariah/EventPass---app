// frontend/js/organizer.js

document.addEventListener('DOMContentLoaded', async () => {
    const myEventsContainer = document.querySelector('#MyEventsContainer') || document.querySelector('.space-y-5') || document.getElementById('events') || document.body.querySelectorAll('div.bg-gradient-to-br, div.bg-slate-800\\/20, div.bg-white')[1] || document.body;
    
    // We target the event feed block automatically based on your UI markup
    const targetFeed = document.getElementById('myEventsFeed') || document.querySelector('main section div') || myEventsContainer;

    await loadOrganizerEvents();

    // Handle form submission for creating a new event
    const createEventForm = document.getElementById('createEventForm') || document.querySelector('form');
    if (createEventForm) {
        createEventForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const titleInput = document.querySelector('input[placeholder="Event Name"]');
            const dateInput = document.querySelector('input[type="date"]');
            const locationInput = document.querySelector('input[placeholder="Location"]');
            const descInput = document.querySelector('textarea[placeholder="Description..."]');
            const capacityInput = document.querySelector('input[placeholder="Capacity"]') || { value: 100 }; // fallback default

            if (!titleInput.value || !dateInput.value || !locationInput.value) {
                alert("Please fill out Name, Date, and Location fields.");
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:5000/create_event', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: titleInput.value,
                        date: dateInput.value,
                        location: locationInput.value,
                        description: descInput.value,
                        capacity: parseInt(capacityInput.value) || 100
                    })
                });

                if (response.ok) {
                    alert("Event posted successfully!");
                    createEventForm.reset();
                    await loadOrganizerEvents(); // reload list
                } else {
                    const errData = await response.json();
                    alert(errData.error || "Failed to create event.");
                }
            } catch (err) {
                console.error("Error posting event:", err);
                alert("Could not connect to server.");
            }
        });
    }
});

// Primary function to load and render organizer events cleanly
async function loadOrganizerEvents() {
    // Dynamically look for the container element where events are listed
    let container = document.getElementById('myEventsContainer') || document.querySelector('.min-h-screen text-slate-100 .space-y-4') || document.querySelector('main .space-y-4') || document.querySelector('.bg-[#0B1E3F] .space-y-4');
    
    // Fallback if structure changes: find the div containing "Python Workshop" from your screen
    if (!container) {
        const headings = Array.from(document.querySelectorAll('h3, h2, div'));
        const sectionHeader = headings.find(el => el.textContent.includes('My Events'));
        if (sectionHeader && sectionHeader.nextElementSibling) {
            container = sectionHeader.nextElementSibling;
        } else {
            container = document.body; // absolute safety fallback
        }
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/get_events');
        const events = await response.json();

        if (!events || events.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8 text-slate-500 text-sm">
                    <i class="fas fa-calendar-plus text-xl mb-2 block"></i> No events created yet.
                </div>`;
            return;
        }

        // Render card layout matching your styling precisely with a clean cursor pointer indicator
        container.innerHTML = events.map(event => {
            const cleanTitle = event.title.replace(/'/g, "\\'");
            const cleanLocation = event.location.replace(/'/g, "\\'");
            const eventCapacity = event.capacity || 100;

            return `
                <div onclick="viewOrganizerEvent(${event.id}, '${cleanTitle}', '${cleanLocation}', '${event.date}', ${eventCapacity})" 
                     class="group bg-[#11254C]/60 hover:bg-[#152e5d]/80 border border-slate-700/30 rounded-2xl p-5 mb-3 flex items-center justify-between cursor-pointer transition-all shadow-md transform active:scale-[0.99]">
                    <div class="truncate pr-4">
                        <h4 class="text-white font-bold text-base group-hover:text-blue-400 transition-colors">${event.title}</h4>
                        <div class="flex items-center gap-4 text-xs text-slate-400 mt-2">
                            <span><i class="far fa-calendar mr-1.5 text-blue-500"></i>${event.date}</span>
                            <span class="truncate"><i class="fas fa-map-marker-alt mr-1.5 text-red-400"></i>${event.location}</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-slate-800/80 group-hover:bg-blue-600 group-hover:text-white text-slate-400 flex items-center justify-center transition-all">
                            <i class="fas fa-chevron-right text-xs"></i>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error("Error loading events window payload:", error);
    }
}

// Click Route Handler navigating to your Attendee Control Center
function viewOrganizerEvent(id, title, location, date, capacity) {
    localStorage.setItem("event_id", id);
    localStorage.setItem("event_title", title);
    localStorage.setItem("event_location", location);
    localStorage.setItem("event_date", date);
    localStorage.setItem("event_capacity", capacity); 
    
    window.location.href = "organizer_details.html";
}