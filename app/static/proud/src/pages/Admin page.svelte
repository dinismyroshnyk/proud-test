<script lang="ts">
    import { onMount } from 'svelte';
    import Footer from "../components/Footer.svelte";
    import Header from "../components/Header.svelte";
    import Menu from "../components/Menu.svelte";

    let value: string = '';
    let members: { email: string }[] = [];
    let num_members: number = -1;
    let requests: any[] = [];
    let emails: any[] = [];
    let title: string = '';
    let content: string = '';

    onMount(async () => {
        await loadMembers();
        await loadRequests();
    });

    async function loadMembers() {
        const response = await fetch('/members', {
            method: 'GET'
        });
        const data = await response.json();
        members = data.members.members_list;
        num_members = data.members.num_members;
        console.log(num_members);
        console.log('Response data:', data);
    }

    async function loadRequests() {
        const response = await fetch('/requests', { method: 'GET' });
        const data = await response.json();
        requests = data.requests;

        await loadEmails();
        matchRequestsWithEmails();
    }

    async function loadEmails() {
        const response = await fetch('/users', { method: 'GET' });
        const data = await response.json();
        emails = data.users;

        console.log('Emails loaded:', emails);
    }

    function matchRequestsWithEmails() {
        if (!emails || emails.length === 0) {
            console.warn('Emails are not loaded or empty');
            return;
        }

        requests.forEach(request => {
            const user = emails.find(email => email.uuid === request.user_id);
            request.email = user ? user.email : 'Unknown';
        });

        console.log('Requests matched with emails:', requests);
    }

    async function sendNotification(event: Event) {
        event.preventDefault();
        try {
            const response = await fetch('/members', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    content,
                    //faltam as imagens
                })
            });
        } catch (error) {
            console.error('Erro ao enviar notificação:', error);
        }
    }

    async function handleRequest(event: Event) {
        event.preventDefault();

        const form = event.target as HTMLFormElement;
        const form_data = new FormData(form);
        const action = form_data.get('action');
        const user_id = form_data.get('user_id');

        if (action === 'approve') {
            try {
                const response = await fetch(`member/${user_id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
            } catch (error) {
                console.error('Erro ao aprovar pedido:', error);
            }
        } else if (action === 'reject') {
            try {
                const response = await fetch(`member/${user_id}/reject/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
            } catch (error) {
                console.error('Erro ao rejeitar pedido:', error);
            }
        }
    }
</script>

<Header />

<div class="dashboard">
    <Menu />
    <div class="dashboard-title">
        <h1>Members</h1>
    </div>

    <div class="members-container">
        <h2>Members</h2>
        <ul class="member-list">
            {#each members as member}
                <li class="member">
                    <img alt="" src="/static/proud/assets/utilizador-circulo.png"><p>{member.email}</p>
                    <!-- não existem redes sociais nem ids para listar -->
                </li>
            {/each}
        </ul>
    </div>
    <div class="requests-container">
        <h2>Requests</h2>
        <ul class="request-list">
            {#each requests as request}
                <li class="request">

                    <form on:submit={handleRequest}>
                        <img alt="" src="/static/proud/assets/utilizador-circulo.png">
                        <p>{request.email}</p>
                        <input type="hidden" name="user_id" value="{request.user_id}" />
                        <button type="submit" name="action" value="approve">Accept</button>
                        <button type="submit" name="action" value="reject">
                            <img alt="" src="/static/proud/assets/eliminar.png">
                        </button>
                    </form>
                </li>
            {/each}
        </ul>
    </div>
    <div class="member-counter">
        <h2>Number of Members</h2>
        <div class="member-number">
            {#if num_members >= 0}
            <p>{num_members}</p>
            {/if}
        </div>
    </div>
    <div class="notify-members">
        <h1>Notify Members</h1>
        <form on:submit={sendNotification}>
            <input
                type="text"
                placeholder="Title"
                bind:value={title}
                required
            />
            <textarea
                rows="5"
                cols="50"
                placeholder="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus porttitor."
                bind:value={content}
                required
            ></textarea>
            <input type="file">
            <!-- falta poder selecionar os emails para enviar a notificação -->

            <button type="submit">Submit</button>
        </form>
    </div>

</div>



<Footer />

