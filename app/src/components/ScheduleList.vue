<template>
    <div class="schedule-list">
        <div
            v-for="event in events"
            :key="event.id"
            class="schedule-list__event d-flex flex-column p-2 my-2"
        >
            <div class="schedule-list__event__details">
                <p>{{ event.name }}</p>
                <p>{{ formatDuration(event) }}</p>
                <p>{{ formateDate(event) }}</p>
            </div>

            <div class="schedule-list__event__footer d-flex justify-content-end">
                <button
                    class="schedule-list__event__delete small"
                    @click="$emit('delete-event', event.id)"
                >
                    Remove Event
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ScheduleList',
    props: {
        events: {
            type: Array,
            required: true
        }
    },
    methods: {
        formatDuration(event) {
            let duration = '';
            if (event.duration['hours'] > 0) {
                duration += `${event.duration['hours']} hours`;
            }

            if (event.duration['minutes'] > 0) {
                if (duration.length > 0) {
                    duration += ' and ';
                }

                duration += `${event.duration['minutes']} minutes`;
            }

            return duration;
        },
        formateDate(event) {
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const event_days = event.days;
            const [hours, minutes] = event.time.split(':').map(Number);
            const event_time = new Date();
            event_time.setHours(hours, minutes, 0, 0); // Set hours and minutes

            let date_string = '';

            if (event.type === 'singular') {
                date_string += days[event_days];
            } else {
                date_string += 'Every ';
                event_days.forEach((day, index) => {
                    date_string += days[day];
                    if (index < event_days.length - 1) {
                        date_string += ', ';
                    }
                });
            }

            date_string += ` at ${event_time.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`;

            return date_string;
        }
    }
}
</script>

<style scoped lang="scss">
.schedule-list {
    &__event {
        box-shadow: 2px 2px 5px rgba(0,0,0, 0.4);
        background-color: white;
        color: rgba(23,23,23);
    }
}

p {
    margin-bottom: 0;
}
</style>
