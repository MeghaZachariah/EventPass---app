document.addEventListener('DOMContentLoaded', () => {
    fetchMyEvents();

    const form = document.getElementById('createEventForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const eventData = {
            title: document.getElementById('eventName').value,
            date: document.getElementById('eventDate').value,
            location: document.getElementById('eventLocation').value,
            description: document.getElementById('eventDesc').value
        };

        try {
            // Replace with your actual Flask endpoint for creating events
            const response = await fetch('http://127.0.0.1:5000/add_event', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(eventData)
            });

            if (response.ok) {
                alert("Event Created Successfully!");
                form.reset();
                fetchMyEvents(); // Refresh the list
            }
        } catch (error) {
            console.error("Error creating event:", error);
        }
    });
});

async function fetchMyEvents() {
    const listContainer = document.getElementById('myEventsList');
    
    try {
        const response = await fetch('http://127.0.0.1:5000/get_events'); 
        const events = await response.json();
        
        document.getElementById('eventCount').innerText = events.length;

        if (events.length === 0) return;

        listContainer.innerHTML = events.map(event => `
            <div class="bg-white/10 border border-slate-700 rounded-2xl p-4 flex justify-between items-center">
                <div>
                    <h3 class="text-white font-medium text-sm">${event.title}</h3>
                    <p class="text-slate-500 text-[11px] mt-1">
                        <i class="far fa-calendar mr-1"></i> ${event.date}
                    </p>
                </div>
                <div class="flex space-x-2">
                    <button class="w-8 h-8 rounded-full bg-slate-800 text-blue-400 flex items-center justify-center">
                        <i class="fas fa-edit text-xs"></i>
                    </button>
                    <button class="w-8 h-8 rounded-full bg-slate-800 text-red-400 flex items-center justify-center">
                        <i class="fas fa-trash text-xs"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error("Error fetching events:", error);
    }
}