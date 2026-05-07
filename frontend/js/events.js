document.addEventListener('DOMContentLoaded', async () => {
    const eventsContainer = document.getElementById('events');

    try {
        // Keeping your actual Flask backend endpoint
        const response = await fetch('http://127.0.0.1:5000/get_events'); 
        const events = await response.json();

        if (!events || events.length === 0) {
            eventsContainer.innerHTML = `<p class="text-slate-500 text-center py-10">No events found today.</p>`;
            return;
        }

        // Mapping your data (using event.title/event.name check) to the premium UI
        eventsContainer.innerHTML = events.map(event => `
            <div class="event-card bg-white rounded-[2rem] p-6 shadow-xl shadow-black/30">
                <div class="flex justify-between items-start mb-4">
                    <div class="pr-4">
                        <h3 class="text-[#0B1E3F] text-xl font-bold leading-tight">${event.title || event.name}</h3>
                        <p class="text-slate-400 text-xs mt-1 font-medium uppercase tracking-wider">EventPass Explorer</p>
                    </div>
                    <div class="bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-[10px] font-black uppercase">
                        Open
                    </div>
                </div>

                <div class="space-y-2 mb-6">
                    <div class="flex items-center text-slate-600 text-sm">
                        <i class="far fa-calendar-alt w-5 text-blue-500"></i>
                        <span class="ml-2">${event.date}</span>
                    </div>
                    <div class="flex items-center text-slate-600 text-sm">
                        <i class="fas fa-map-marker-alt w-5 text-red-400"></i>
                        <span class="ml-2">${event.location}</span>
                    </div>
                </div>

                <button onclick="viewEvent(${event.id}, '${(event.title || event.name).replace(/'/g, "\\'")}', '${event.location}', '${event.date}')" 
                        class="w-full bg-[#0B1E3F] text-white py-4 rounded-2xl font-bold text-sm hover:bg-[#142B5F] transition-all shadow-lg shadow-blue-900/20">
                    Get Details
                </button>
            </div>
        `).join('');

    } catch (error) {
        console.error("Error fetching events:", error);
        eventsContainer.innerHTML = `<p class="text-red-400 text-center py-10">Cannot connect to server. Ensure Flask is running.</p>`;
    }
});

// Merged function to handle storage and navigation
function viewEvent(id, title, location, date) {
    localStorage.setItem("event_id", id);
    localStorage.setItem("event_title", title);
    localStorage.setItem("event_location", location);
    localStorage.setItem("event_date", date);
    
    // Redirecting to your new details page
    window.location.href = "event_details.html";
}