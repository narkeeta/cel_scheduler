<template>
  <div class="scheduler mt-5">
    <h1 class="text-center">Schedule</h1>

    <button v-if="!show_form" @click="showAddEventForm" class="w-100">Add Event</button>

    <event-form v-if="show_form" @added-event="addEvent"/>

    <schedule-list
        v-else
        :events="sorted_events"
        @delete-event="deleteEvent"
        @cancel="cancelAddingEvent"
    />
  </div>
</template>

<script>
import axios from 'axios';
import EventForm from '@/components/EventForm.vue';
import ScheduleList from '@/components/ScheduleList.vue'

export default {
    name: 'Scheduler',
    components: {
        EventForm,
        ScheduleList
    },
    data() {
        return {
            events: [],
            show_form: false,
        }
    },
    computed: {
        current_date() {
            return new Date().getDay();
        },
        sorted_events() {
            return this.events.sort((a, b) => {
                const a_first_date = a.days[0];
                const b_first_date = b.days[0];

                if (a_first_date === b_first_date) {
                    return a.time.localeCompare(b.time);
                }

                return a_first_date - b_first_date;
            });
        }
    },
    mounted() {
        this.getEvents();
    },
    methods: {
        async getEvents() {
            try {
                const response = await axios.get('/events/list');
                this.events = response.data.map(event => {
                    event.days = JSON.parse(event.days).sort();
                    event.duration = JSON.parse(event.duration);
                    return event;
                });
            } catch (error) {
                console.error(error);
            }
        },
        showAddEventForm() {
            this.show_form = true;
        },
        async addEvent() {
            this.show_form = false;
            this.getEvents();
        },
        async deleteEvent(id) {
            try {
                await axios.delete(`/event/delete/${id}`);
                this.getEvents();
            } catch (error) {
                console.error(error);
            }
        },
        cancelAddingEvent() {
            this.show_form = false;
        }
    }
}
</script>

<style lang="scss">
$primary-color: #ef483e;
$primary-hover: darken($primary-color, 20%);
.scheduler {
    width:80%;
    max-width: 1000px;
    margin: 0 auto;

    button {
        padding: .25em .5em;
        border: none;
        background-color: $primary-color;
        color: white;
        cursor: pointer;
        font-weight:bolder;
        transition: .3s ease;

        &:hover {
            background-color: $primary-hover;
        }

        &:disabled {
            background-color: gray;
            cursor: not-allowed;
        }
    }
}
</style>